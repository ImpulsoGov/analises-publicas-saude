using JuMP
using Ipopt
using Printf
using Plots
using RollingFunctions
using CSV
using DataFrames
using Measures
using Dates
import StatsBase.geomean
import Statistics.mean, Statistics.median

struct SEIR_Parameters
    ndays::Int64
    s0::Float64
    e0::Float64
    i0::Float64
    r0::Float64
    natural_rt::Float64
    tinc::Float64
    tinf::Float64
    SEIR_Parameters(ndays, s0, e0, i0, r0) = new(ndays, s0, e0, i0, r0, 2.5, 5.2, 2.9)
end


function mostra_populacao(pop)
    if pop < 1000
        return @sprintf("%.1f", pop)
    elseif pop < 1000000
        return @sprintf("%.1fK", pop/ 1000)
    else
        return @sprintf("%.1fM", pop / 1000000)
    end
end

formata_data = x -> Dates.format(x, "dd/mm/yyyy")


function imprime_lista_com_datas(lista, hoje)
    um_dia = Day(1)
    data = hoje + um_dia
    for l in lista[1:end - 1]
        print(l, " (", Dates.format(data, "dd/mm"), "), ")
        data += um_dia
    end
    println(lista[end], " (", Dates.format(data, "dd/mm"), ").")
end


function seir_grad(m, s, e, i, r, rt, tinf, tinc)
    ds = @NLexpression(m, -(rt/tinf)*s*i)
    de = @NLexpression(m, (rt/tinf)*s*i - (1.0/tinc)*e)
    di = @NLexpression(m, (1.0/tinc)*e - (1.0/tinf)*i)
    dr = @NLexpression(m, (1.0/tinf)*i)
    return ds, de, di, dr
end


function seir_model_with_free_initial_values(iparam)
    m = Model(optimizer_with_attributes(Ipopt.Optimizer, "print_level" => 0, "sb" => "yes"))
    # For simplicity I am assuming that one step per day is OK.
    dt = 1.0

    # State variables
    lastday = iparam.ndays - 1
    @variable(m, 0.0 <= s[0:lastday] <= 1.0)
    @variable(m, 0.0 <= e[0:lastday] <= 1.0)
    @variable(m, 0.0 <= i[0:lastday] <= 1.0)
    @variable(m, 0.0 <= r[0:lastday] <= 1.0)
    @variable(m, 0.0 <= rt[0:lastday] <= iparam.natural_rt)

    # Note that I do not fix the initial state. It should be defined elsewhere.

    # Implement Haun's method
    for t = 1:lastday
        ds, de, di, dr = seir_grad(m, s[t - 1], e[t - 1], i[t - 1], r[t - 1], rt[t - 1], iparam.tinf, iparam.tinc)

        sp = @NLexpression(m, s[t - 1] + ds*dt)
        ep = @NLexpression(m, e[t - 1] + de*dt)
        ip = @NLexpression(m, i[t - 1] + di*dt)
        rp = @NLexpression(m, r[t - 1] + dr*dt)

        dsp, dep, dip, drp = seir_grad(m, sp, ep, ip, rp, rt[t], iparam.tinf, iparam.tinc)

        @NLconstraint(m, s[t] == s[t - 1] + 0.5*(ds + dsp)*dt)
        @NLconstraint(m, e[t] == e[t - 1] + 0.5*(de + dep)*dt)
        @NLconstraint(m, i[t] == i[t - 1] + 0.5*(di + dip)*dt)
        @NLconstraint(m, r[t] == r[t - 1] + 0.5*(dr + drp)*dt)
    end
    return m
end


function seir_model(iparam)
    m = seir_model_with_free_initial_values(iparam)

    # Initial state
    s0, e0, i0, r0 = m[:s][0], m[:e][0], m[:i][0], m[:r][0]
    fix(s0, iparam.s0; force=true)
    fix(e0, iparam.e0; force=true)
    fix(i0, iparam.i0; force=true)
    fix(r0, iparam.r0; force=true)

    return m
end


function fixed_rt_model(iparam)
    lastday = iparam.ndays - 1
    m = seir_model(iparam)
    rt = m[:rt]

    # Fix all rts
    for t = 1:lastday
        fix(rt[t], iparam.natural_rt; force=true)
    end
    return m
end


"""
    estima_rt_total_var

    Estima os rt diários que explicam uma curva de infectados usando
    uma regularização de variação total.
"""
function estima_rt_total_var(infectados, max_rt=10.0)
    # Cria modelo SEIR e ajusta paramêtros tentando achar a evolução do rt
    ndias = length(infectados)
    iparam = SEIR_Parameters(ndias, 1.0, 0.0, 0.0, 0.0)
    m = seir_model_with_free_initial_values(iparam)
    lastday = iparam.ndays - 1

    # Define estado inicial
    s0, e0, i, r0, rt = m[:s][0], m[:e][0], m[:i], m[:r][0], m[:rt]
    set_start_value(r0, iparam.r0)
    set_start_value(s0, iparam.s0)
    set_start_value(e0, iparam.e0)
    set_start_value(i[0], iparam.i0)

    # Ajusta o limitante superior dos rts para um valor alto pré-determinando nesse arquivo.
    for d = 0:lastday
        set_upper_bound(rt[d], max_rt)
    end

    # Restrição para calular a variação total
    @variable(m, ttv[1:lastday])
    @constraint(m, con_ttv[i=1:lastday], ttv[i] >= (rt[i - 1] - rt[i])^2)
    #@constraint(m, con_ttv2[i=1:lastday], ttv[i] >= (rt[i] - rt[i - 1])^2)

    # As proporções somam 1
    @constraint(m, s0 + e0 + i[0] + r0 == 1.0)

    # Compute a scaling factor so as a least square objetive makes more sense
    valid = (t for t = 0:lastday if infectados[t + 1] > 0)
    @NLobjective(m, Min, sum((i[t]/infectados[t + 1] - 1.0)^2 for t in valid) + 0.25*sum(ttv[t] for t = 1:lastday))
    optimize!(m)
    i_est, rt_est = value.(m[:i]).data, value.(m[:rt]).data;
    
    return i_est, rt_est
end