.PHONY: all clean

all: data metagenomes

clean:
	rm -rf data

metagenomes: data/metagenome_list.pkl $(patsubst %, %.fna.gz, $(shell python scripts/metagenome_list.py data/metagenome_list.pkl))

list: data data/metagenome_list.pkl

data:
	mkdir data

data/metagenome_list.pkl: scripts/get_metagenome_list.py
	python $< $@

%.fna.gz: data/metagenome_list.pkl scripts/download_metagenomes.py
	python scripts/download_metagenomes.py $< data/
