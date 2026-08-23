.PHONY: validate validate-network

validate:
	python3 scripts/validate.py

validate-network:
	python3 scripts/validate.py --network
