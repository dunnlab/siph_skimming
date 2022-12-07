library(tidyverse)
library(ggpubr)
library(cowplot)

D = read.csv("output/genome_size_report.tsv", sep="\t", header=TRUE) %>%
  separate(sample, c("species", "sample_id", "coverage"), sep="_" ) %>%
  mutate(coverage = str_replace(coverage, "x", "") ) %>%
  mutate(coverage = as.numeric(coverage)) %>%
  mutate(bp=read_count*150) %>%
  mutate(min_hap_len_gb=min_hap_len/1e9) %>%
  mutate(repeat_percent = min_rep_len/min_hap_len*100) %>%
  mutate(species=str_replace(species, "-", " ")) %>%
  mutate(species=str_replace(species, "Chelophyes", "Chelophyes appendiculata")) %>%
  filter(!grepl('Resomia', species))

p_size = D %>%
  ggplot(aes(x=coverage, y=min_hap_len_gb)) + 
  geom_line(aes(linetype = species)) + 
  ylab("haploid length (Gb)") +
  theme_classic()

p_het = D %>%
  ggplot(aes(x=coverage, y=min_het)) + 
  geom_line(aes(linetype = species)) + 
  ylab("heterozygosity (%)") +
  theme_classic()

p_rep = D %>%
  ggplot(aes(x=coverage, y=repeat_percent)) + 
  geom_line(aes(linetype = species)) + 
  ylab("repeat (%)") +
  theme_classic()

figure <- ggarrange(
  p_size + theme(legend.position = "none"), 
  p_het + theme(legend.position = "none"), 
  p_rep + theme(legend.position = "none"),
  get_legend(p_size),
  labels = c("A", "B", "C", NA),
  ncol = 2, nrow = 2)

ggsave(
  "figure_rarefaction_lines.png", 
  figure,
  width=6.5,
  height=6,
  units="in"
  )
