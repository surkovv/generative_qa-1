from copy import deepcopy
from deeppavlov import build_model, configs
from udapi.block.read.conllu import Conllu
import deeppavlov.models.torch_bert.torch_generative_qa 
from io import StringIO


class LongAnswerPreprocessor:
    
    def __init__(self):
        self.model = build_model(configs.syntax.syntax_ru_syntagrus_bert, download=True)
        self.handlers = [self.general_case,
                         self.parent_removal_case,
                         self.whether_case]

    def process_batch(self, batch, answer_batch):
        return [self.process_parse(parse, answer) for parse, answer in zip(self.model(batch), answer_batch)]

    def process_parse(self, parse, answer):
        
        if answer[-1] == '.':
            answer = answer[:-1]
        print(parse, end='\n\n')

        tree = Conllu(filehandle=StringIO(parse)).read_tree()
        for handler in self.handlers:
            result = handler(deepcopy(tree), answer)
            if result is not None:
                
                mark_node = self.find_node_like(result, ['?'])
                if mark_node is not None:
                    mark_node.form = '.'
                long_answer = result.get_sentence()
                long_answer = long_answer[0].upper() + long_answer[1:]
                return long_answer
        
        return answer

    def find_root(self, tree):
        for node in tree.descendants:
            if node.deprel == "root" and node.children:
                return node

    def find_node_like(self, tree, word_list):
        for node in tree.descendants:
            if node.form.lower() in word_list:
                return node
        return None
    
    def restore_subj_root_obj_order(self, tree):
        subj, root, objs, others = None, self.find_root(tree), [], []
        if root is None:
            return
        for node in root.children:
            if node.udeprel == 'nsubj':
                subj = node
            elif node.udeprel in ['obl', 'det', 'advmod'] and node.form != 'не':
                others.append(node)
            elif node.udeprel in ['obj', 'iobj']:
                objs.append(node)

        qmark = self.find_node_like(tree, ['?'])
        if subj and root:
            subj.shift_before_subtree(root)
        
        for obj in objs:
            if qmark and obj:
                obj.shift_before_node(qmark)
            elif obj and root:
                obj.shift_after_subtree(root)
        
        for other in others:
            if qmark and other:
                other.shift_before_node(qmark)
            elif other and root:
                other.shift_after_subtree(root)


    def general_case(self, tree, answer):
        '''
        Removes a question word and all its dependent words
        '''

        key_words = [
            'кто',
            'сколько',
            'что',
            'кого',
            'чего',
            'кем',
            'чем',
            'кому',
            'чему',
            'ком',
            'чём',
            'когда',
            'где',
            'куда',
            'откуда'
        ]
        
        qword_node = self.find_node_like(tree, key_words)
        if qword_node is None:
            return None
        
        if qword_node.udeprel == 'root':
            return None

        qword_node.form = answer 
        for child in qword_node.children:
            child.remove()
        
        self.restore_subj_root_obj_order(tree)
        return tree

    def parent_removal_case(self, tree, answer):
        '''
        Removes parent node of question word and all its descendants
        '''
        
        key_words = [
            'какой',
            'какого',
            'какому',
            'каким',
            'каком',
            'какая',
            'какой',
            'какую',
            'какое',
            'какие',
            'каких',
            'каким',
            'какими',
        ]

        qword_node = self.find_node_like(tree, key_words)
        if qword_node is None or qword_node.parent is None:
            return None

        stop_words = [
            'стал',
            'стала',
            'стало',
            'стали',
            'должен',
            'должна',
            'должны',
            'должно'
        ]

        needed_node = qword_node.parent

        if needed_node.form in stop_words:
            needed_node = qword_node
        elif qword_node.udeprel == 'root' or qword_node.parent.is_root():
            return None
        
        print(needed_node)
        if needed_node.udeprel == 'root':
            return None

        needed_node.form = answer
        for child in needed_node.children:
            child.remove()

        self.restore_subj_root_obj_order(tree)
        return tree
    
    def whether_case(self, tree, answer):
        '''
        If 'ли' is direct children of root, then replace root with answer and put root after subject subtree
        otherwise, replace respective subtree with answer

        Examples:
        1. [Зависит ли форма генома от типа нуклеиновой кислоты? (не зависит)]
        -> Форма генома не зависит от типа нуклеиновой кислоты.
        2. [Многие ли верят в одновременное существование материального тела и нематериального сознания? (большинство людей на Земле)']
        -> Большинство людей на Земле верят одновременное существование материального тела и нематериального сознания.
        3. [Многие ли вещества входящие в растворители токсичны? (Многие синтетические проявляющие вещества)]
        -> Многие синтетические проявляющие вещества входящие в растворители токсичны.
        '''

        whether_node = self.find_node_like(tree, ['ли']) 

        if whether_node is None or whether_node.parent is None:
            return None

        if whether_node.parent.udeprel == 'root':
            # case 1
            needed_node = whether_node.parent 
            whether_node.remove()
            needed_node.form = answer
            subj_node = None
            for child in needed_node.children:
                if child.udeprel == 'nsubj':
                    subj_node = child
            if subj_node is None:
                return None
            needed_node.shift_after_subtree(subj_node, without_children=True)
            self.restore_subj_root_obj_order(tree)
            return tree
        
        needed_node = whether_node
        while needed_node.udeprel not in ['nsubj', 'root']:
            needed_node = needed_node.parent

        if needed_node.udeprel == 'root':
            return None

        for child in needed_node.children:
            child.remove()

        needed_node.form = answer

        self.restore_subj_root_obj_order(tree)
        return tree

a = LongAnswerPreprocessor()

questions = ['Когда происходит прямой переход графита в алмаз?', 
             'Чем представлена у рыб система кровообращения?',
             'В каком городе первый в мире городской автобус с двигателем внутреннего сгорания вышел на маршрут?',
             'Каким стал стиль последних работ художника?',
             'Какая статья и пункт дает возможность для легализации ПО, скачанного из Интернет и предоставляемого по лицензии GNU GPL?',
             'Зависит ли форма генома от типа нуклеиновой кислоты?',
             'Многие ли верят в одновременное существование материального тела и нематериального сознания?',
             'Многие ли вещества входящие в растворители токсичны?',
             'что в режиме гибернации отключается?',
             'Что содержат белки-каналы?',
             'Для чего используется добавка фторидов в соль?',
             'Находит ли отражение в алфавите фонетическая связь слогов?',
             'Сколько раз Реджинальд Дохерти стал чемпионом с 1897 по 1900 год?',
             'Где колючие кустарники и засухоустойчивые злаки формируют земную кору?',
             'Какие дела не вел Московский судный приказ?',
             'Кому передали Озерки родители Бунина?'
             ]
answers = ['при 3000 K и давлении 11—12 ГПа', 'только одним замкнутым контуром', 
           'в Лондоне', 'нервным и гнетущим', 'пункт 2 статьи 434',
           'не зависит',
           'большинство людей на Земле',
           'Многие синтетические проявляющие вещества.',
           'питание ОЗУ',
           'Внутренние заполненные водой поры',
           'для профилактики зубных заболеваний',
           'не находит',
           'четыре раза подряд',
           'Только на участках, где появляется вода',
           'об убийстве, разбое и воровстве с поличным',
           'сыну Евгению',
           ]

print(*a.process_batch(questions, answers), sep='\n') 
name = 'dev-v1.1.json'
import json
from tqdm import tqdm

#exit(0)

with open(name, 'r') as f:
    dataset = json.load(f)['data'][0]['paragraphs']
    for record in tqdm(dataset):
        for q_record in record['qas']:
            question = q_record['question']
            if question.find('?') not in [-1, len(question) - 1]:
                question = question.replace('?', '') + '?'
            for ans_record in q_record['answers']:
                try:
                    ans_record['long_text'] = a.process_batch([question], [ans_record['text']])[0]
                except:
                    ans_record['long_text'] = ans_record['text']

with open(name[:-5] + 'long.json', 'w', encoding='utf8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)
