# QA model with augmented answers

We fine-tuned T5-base and T5-small on adjusted <em>MS Marco v2.1</em> dataset (https://arxiv.org/pdf/1611.09268v3.pdf). 
The dataset was cleaned of excessively long, corrupted and "gibberish" records.

### Metrics

    T5-small: {"squad_v1_f1": 0.6287, "sacrebleu": 8.323}
    T5-base: {"squad_v1_f1": 0.7634, "sacrebleu": 11.8706}

### Examples (t5-small)   

    question: 'Who played Sheldon Cooper in The Big Bang Theory'
    context: ['Sheldon Lee Cooper is a fictional character in the CBS television series The Big Bang Theory and its spinoff series Young Sheldon, portrayed by actors Jim Parsons']
    output: 'Sheldon Cooper is portrayed by Jim Parsons in The Big Bang Theory.'
    
    question1: 'What is the capital of Russia?'
    question2: 'How many people live in Moscow?'
    question3: 'river in Moscow'
    context: ["Moscow is the capital and largest city of Russia. The city stands on the Moskva River in Central Russia, with a population estimated at 12.4 million residents within the city limits, over 17 million residents in the urban area, and over 20 million residents in the metropolitan area. The city covers an area of 2,511 square kilometers (970 sq mi), while the urban area covers 5,891 square kilometers (2,275 sq mi), and the metropolitan area covers over 26,000 square kilometers (10,000 sq mi). Moscow is among the world's largest cities; being the most populous city entirely in Europe, the largest urban and metropolitan area in Europe, and the largest city by land area on the European continent."]
    output1: 'Moscow is the capital and largest city of Russia.'
    output2: 'There are 12.4 million people live in Moscow.'
    output3: 'Moskva River is in Moscow.'
    
  ### Possible enhancements
  
  T5-base fine-tuning was slightly impaired: the dataset included too large answers, while config had tight limit for generated answer. Thus, the model tend to cut
  answers thereby generating incomplete sentences despite decent metrics scores. Refinetuning with new config worths considering.
  
  
