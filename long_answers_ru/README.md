# QA model with augmented answers (russian)

The model is fune-tuned [ruT5-base](https://huggingface.co/sberbank-ai/ruT5-base) on [SberQuad](https://arxiv.org/abs/1912.09723) with generated long answers. 
First, I implemented an algorithm that yields a long answer using the short answer and the question (`preprocessing.py`). Then I excluded very short answers from dataset
and finetuned ruT5-base on it.

### Metrics
From fusion-in-decoder:
    
    "squad_v1_f1": 11.6561, "sacrebleu": 54.0081

### Examples

    question1: 'Кто играет Шелдона Купера?'
    question2: 'В каком сериале снимался Джим Парсонс?'
    context: ['Шелдон Ли Купер — вымышленный персонаж, один из главных героев телесериала «Теория Большого взрыва» и его спин-оффа «Детство Шелдона». Роль Шелдона Купера в «Теории Большого взрыва» исполняет Джим Парсонс, получивший за неё премии «Эмми»']
    output1: 'Джим Парсонс играет Шелдона Купера.' 
    output2: 'Джим Парсонс снимался в Теории Большого взрыва.'
    
    question1: 'Где родился Лев Толстой?'
    question2: 'Из-за чего умерла мать Толстого?'
    context: ['Лев Николаевич Толстой родился 28 августа 1828 года в Крапивенском уезде Тульской губернии, в наследственном имении матери — Ясной Поляне. Был четвёртым ребёнком в семье. Мать умерла в 1830 году от «родовой горячки», как тогда говорили, через полгода после рождения дочери, когда Льву не было ещё и трёх лет.']
    output1: 'Лев Толстой родился в Крапивенском уезде Тульской губернии.'
    output2: 'Мать Толстого умерла от-родовой горячки.'
    
### Possible enhancements
The long answers are not always gramatically correct. One can find a dataset with long answers or make the prepropessing algorithm more detailed.
