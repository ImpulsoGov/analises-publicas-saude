create-env:
	virtualenv .internal_analysis
	source .internal_analysis/bin/activate; \
		pip3 install -r requirements.txt; \
		sudo apt update; \
		sudo apt install r-base; \
		python -m ipykernel install --user --name=internal_analysis

# sudo -H pip3 install -U -r requirements.txt 
