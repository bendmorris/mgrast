metagenomes: data/metagenome_list.pkl $(patsubst %, %.fna.gz, $(shell python scripts/metagenome_list.py data/metagenome_list.pkl))

list: data/metagenome_list.pkl

data/metagenome_list.pkl: scripts/get_metagenome_list.py
	python $< $@

%.fna.gz: data/metagenome_list.pkl scripts/download_metagenomes.py
	python scripts/download_metagenomes.py $< data/
