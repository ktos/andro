#!/usr/bin/env python
# coding: utf-8

# In[17]:


import re

with open('../ap.tex', 'r', encoding='utf-8') as f:
    data = f.read()
    
words = []


# In[18]:


words = re.findall(r"\[(.*?)\]", data)


# In[19]:


with open('speech.txt', 'w', encoding='utf-8') as f2:
    f2.writelines((x + '\n' for x in words))

