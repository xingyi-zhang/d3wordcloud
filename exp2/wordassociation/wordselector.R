library(dplyr)
library(rstudioapi)

setwd(dirname(getActiveDocumentContext()$path))

a1 <- read.csv(file = "AppendixA1.csv")
a2  <- read.csv(file = "AppendixA2.csv")
freq_dict <- read.csv(file = "SUBTLEXusfrequency.csv")
bad_dict <- read.csv(file = "badword.csv", header = FALSE) 
bad_list <- bad_dict$V1

a <- rbind(a1,a2)

freq_dict <- freq_dict %>% 
  select(Word,SUBTLWF) %>%
  mutate(Targets = toupper(Word))  %>%
  rename(word_freq = SUBTLWF) 

word_dict <- a %>% 
  select(Cues,Targets,Forward.Strength,Mediated.Strength) %>% 
  filter(nchar(Targets)>5) %>%
  filter(Forward.Strength>0.025) 

targets <- inner_join(freq_dict,word_dict,by = "Targets") %>%
  select(-Targets)

target_filtered <- targets %>% 
  count(Word) %>%
  filter(n>19)


target_dict <- inner_join(targets,target_filtered, by = "Word") %>%
  filter(word_freq <500) %>%
  mutate(targets = toupper(Word),cues = tolower(Cues)) %>%
  select(targets,cues,Forward.Strength) %>%
  filter(! cues %in% bad_list) %>%
  group_by(targets) %>%
  arrange(desc(Forward.Strength), cues) %>%
  mutate(num = 1:n()) %>%
  filter(num <21) %>%
  select(targets,cues) %>%
  arrange(targets,cues)

all_targets <- distinct(target_dict,targets) %>%
  rename(Targets = targets)

write.csv(all_targets,"all_targets.csv")

all_cues <- inner_join(all_targets,word_dict, by = "Targets") %>%
  mutate(cues = tolower(Cues)) %>%
  filter(!cues %in% bad_list) %>%
  rename(targets = Targets) %>%
  select(targets,cues)

write.csv(target_dict,"target_dict.csv")
write.csv(all_cues,"all_cues.csv")