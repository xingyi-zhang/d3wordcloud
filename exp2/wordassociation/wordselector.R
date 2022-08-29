library(dplyr)
library(rstudioapi)

setwd(dirname(getActiveDocumentContext()$path))

a1 <- read.csv(file = "AppendixA1.csv")
a2  <- read.csv(file = "AppendixA2.csv")
freq_dict <- read.csv(file = "SUBTLEXusfrequency.csv")
bad_dict <- read.csv(file = "badword.csv", header = FALSE) 
bad_list <- bad_dict$V1
sensitive_list = c('church','police','alcohol','religion','government','stupid')

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
  filter(! Word %in% sensitive_list) %>%
  filter(n<=25)

target_dict <- inner_join(targets,target_filtered, by = "Word") %>%
  filter(word_freq <500) %>%
  mutate(targets = toupper(Word),cues = tolower(Cues)) %>%
  select(targets,cues,Forward.Strength) %>%
  filter(! cues %in% bad_list) %>%
  group_by(targets) %>%
  arrange(desc(Forward.Strength), cues) %>%
  mutate(num = 1:n()) %>%
  filter(num <26) %>%
  mutate(mean_strength = mean(Forward.Strength),maxnum = max(num))

target_dict<-target_dict %>%
  arrange(desc(maxnum),desc(mean_strength))%>%
  select(targets,cues)
write.csv(target_dict,"target_dict.csv")


all_targets <- distinct(target_dict,targets) %>%
  rename(Targets = targets)

write.csv(all_targets,"all_targets.csv")

all_cues <- inner_join(all_targets,word_dict, by = "Targets") %>%
  mutate(cues = tolower(Cues)) %>%
  filter(!cues %in% bad_list) %>%
  rename(targets = Targets) %>%
  select(targets,cues)

write.csv(all_cues,"all_cues.csv")



### strength check
strength_check <-target_dict %>%
  group_by(targets) %>%
  summarize(mean_strength = mean(Forward.Strength))

write.csv(strength_check,"strength_check.csv")

