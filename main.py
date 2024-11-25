import re
from pyswip import Prolog


prolog = Prolog()
prolog.consult("family.pl") 


def match_pattern(user_input):

   
    patterns = {

        "Who siblings_q": r"Who are the siblings of (.+)\?",
        "Who sisters_q": r"Who are the sisters of (.+)\?",
        "Who brothers_q": r"Who are the brothers of (.+)\?",
        "Who mother_q": r"Who is the mother of (.+)\?",
        "Who father_q": r"Who is the father of (.+)\?",
        "Who parents_q": r"Who are the parents of (.+)\?",
        "Who daughters_q": r"Who are the daughters of (.+)\?",
        "Who sons_q": r"Who are the sons of (.+)\?",
        "Who children_q": r"Who are the children of (.+)\?",
       
        "siblings": r"(.+) and (.+) are siblings\.",
        "brother": r"(.+) is a brother of (.+)\.",
        "sister": r"(.+) is a sister of (.+)\.",
        "father": r"(.+) is the father of (.+)\.",
        "mother": r"(.+) is the mother of (.+)\.",
        "parents": r"(.+) and (.+) are the parents of (.+)\.",
        "grandmother": r"(.+) is a grandmother of (.+)\.",
        "grandfather": r"(.+) is a grandfather of (.+)\.",
        "child": r"(.+) is a child of (.+)\.",
        "children": r"(.+),(.+) and (.+) are children of (.+)\.",
        "daughter": r"(.+) is a daughter of (.+)\.",
        "son": r"(.+) is a son of (.+)\.",
        "uncle": r"(.+) is an uncle of (.+)\.",
        "aunt": r"(.+) is an aunt of (.+)\.",
        

        "siblings_q": r"Are (.+) and (.+) siblings\?",
        "sister_q": r"Is (.+) a sister of (.+)\?",
        "brother_q": r"Is (.+) a brother of (.+)\?",
        "mother_q": r"Is (.+) the mother of (.+)\?",
        "father_q": r"Is (.+) the father of (.+)\?",
        "parents_q": r"Are (.+) and (.+) the parents of (.+)\?",
        "grandmother_q": r"Is (.+) a grandmother of (.+)\?",
        "grandfather_q": r"Is (.+) a grandfather of (.+)\?",
        "daughter_q": r"Is (.+) a daughter of (.+)\?",
        "son_q": r"Is (.+) a son of (.+)\?",
        "child_q": r"Is (.+) a child of (.+)\?",
        "children_q": r"Are (.+) and (.+) children of (.+)\?",
        "uncle_q": r"Is (.+) an uncle of (.+)\?",
        "aunt_q": r"Is (.+) an aunt of (.+)\?",
        "relatives_q": r"Are (.+) and (.+) relatives\?",
    }

    for pattern_type, pattern in patterns.items():
        match = re.match(pattern, user_input)
        if match:
            return pattern_type, match.groups()
    return None, None


def check_for_circular_relationship(parent, child):
   
    def get_ancestors(person):
        ancestors = set()
        parents = list(prolog.query(f"parent(P, {person.lower()})"))
        while parents:
            for parent in parents:
                ancestors.add(parent["P"].lower())
                
                parents = list(prolog.query(f"parent(P, {parent['P'].lower()})"))
        return ancestors
    
    parent_ancestors = get_ancestors(parent)
    child_ancestors = get_ancestors(child)
    
    if parent.lower() in child_ancestors or child.lower() in parent_ancestors:
        return True
    
    return False


def check_multiple_parents(child):
    existing_mother = list(prolog.query(f"mother(X, {child.lower()})"))
    if existing_mother:
        return True 

    existing_father = list(prolog.query(f"father(X, {child.lower()})"))
    if existing_father:
        return True
    return False 

def existing_parents(child):
    existing_mother = list(prolog.query(f"mother(X, {child.lower()})"))
    if existing_mother:
        return "mother"  

    existing_father = list(prolog.query(f"father(X, {child.lower()})"))
    if existing_father:
        return "father"  

    return None  

def check_if_mother_exists(child, mother):
    existing_mother = list(prolog.query(f"mother(X, {child.lower()})"))
    return bool(existing_mother)


def check_if_father_exists(child, father):
    existing_father = list(prolog.query(f"father(X, {child.lower()})"))
    return bool(existing_father)

def assert_if_not_exists(fact):
    existing_fact = list(prolog.query(fact))
    
    if existing_fact:
        return f"The fact '{fact}' already exists. No duplicate assertion made."
    
    prolog.assertz(fact)
    return f"Successfully asserted the fact '{fact}'."

def is_parent_or_child(person1, person2):
    parent_fact = list(prolog.query(f"mother({person1.lower()}, {person2.lower()})"))
    if parent_fact:
        return True
    
    parent_fact = list(prolog.query(f"mother({person2.lower()}, {person1.lower()})"))
    if parent_fact:
        return True
    
    parent_fact = list(prolog.query(f"father({person1.lower()}, {person2.lower()})"))
    if parent_fact:
        return True
    
    parent_fact = list(prolog.query(f"father({person2.lower()}, {person1.lower()})"))
    if parent_fact:
        return True

    return False

def is_grandparent(person1, person2):
    grandparent_fact = list(prolog.query(f"grandmother({person1.lower()}, {person2.lower()})"))
    if grandparent_fact:
        return True
    
    grandparent_fact = list(prolog.query(f"grandmother({person2.lower()}, {person1.lower()})"))
    if grandparent_fact:
        return True
    
    grandparent_fact = list(prolog.query(f"grandfather({person1.lower()}, {person2.lower()})"))
    if grandparent_fact:
        return True
    
    grandparent_fact = list(prolog.query(f"grandfather({person2.lower()}, {person1.lower()})"))
    if grandparent_fact:
        return True

    return False

def is_aunt_uncle(person1, person2):
    aunt_fact = list(prolog.query(f"aunt({person1.lower()}, {person2.lower()})"))
    if aunt_fact:
        return True
    
    aunt_fact = list(prolog.query(f"aunt({person2.lower()}, {person1.lower()})"))
    if aunt_fact:
        return True
    
    uncle_fact = list(prolog.query(f"uncle({person1.lower()}, {person2.lower()})"))
    if uncle_fact:
        return True
    
    uncle_fact = list(prolog.query(f"uncle({person2.lower()}, {person1.lower()})"))
    if uncle_fact:
        return True

    return False


def is_sibling(person1, person2):
    sibling_fact = list(prolog.query(f"sibling({person1.lower()}, {person2.lower()})"))
    if sibling_fact:
        return True
    
    sibling_fact = list(prolog.query(f"sibling({person2.lower()}, {person1.lower()})"))
    if sibling_fact:
        return True
    
    sister_fact = list(prolog.query(f"sister({person1.lower()}, {person2.lower()})"))
    if  sister_fact:
        return True
    
    sister_fact = list(prolog.query(f"sister({person2.lower()}, {person1.lower()})"))
    if  sister_fact:
        return True
    
    brother_fact = list(prolog.query(f"brother({person1.lower()}, {person2.lower()})"))
    if brother_fact:
        return True
    
    brother_fact = list(prolog.query(f"brother({person2.lower()}, {person1.lower()})"))
    if brother_fact:
        return True

    return False

def check_if_parent_exists(child, parent):
    existing_parent = list(prolog.query(f"parent({parent.lower()}, {child.lower()})"))
    return bool(existing_parent)




def process_statement(pattern_type, args):
    try:
        def check_gender_compatibility(person, expected_gender):
            existing_male = list(prolog.query(f"male({person.lower()})"))
            existing_female = list(prolog.query(f"female({person.lower()})"))
            
            if not existing_male and not existing_female:
                return True  
            if expected_gender == "male" and existing_female:
                return False 
            elif expected_gender == "female" and existing_male:
                return False 
            return True 
        
        if len(set(args)) != len(args):
            return "A person cannot have two different relationships with themselves."

        if pattern_type == "siblings":
            person1, person2 = args
            if person1.lower() == person2.lower():
                return "A person cannot be their own sibling."
            
            if is_parent_or_child(person1, person2):
                return f"{person1} cannot be a sibling to {person2} due to an existing parent/child relationship."

            if is_sibling(person1, person2):
                return f"{person1} cannot be a sibling to {person2} due to an sibling relationship."
            
            if is_aunt_uncle(person1, person2):
                return f"{person1} cannot be a sibling to {person2} due to an existing relationship."
            
            if is_grandparent(person1, person2):
                return f"{person1} cannot be a sibling to {person2} due to an existing relationship."
            
       
            parents1 = list(prolog.query(f"parent(P, {person1.lower()})"))
            parents2 = list(prolog.query(f"parent(P, {person2.lower()}))"))
            
            if not parents1 or not parents2:
                return f"No common parent found for {person1} and {person2}."

            for parent in parents1:
                parent_name = parent['P']
                prolog.assertz(f"parent({parent_name}, {person2.lower()})")
            
            for parent in parents2:
                parent_name = parent['P']
                prolog.assertz(f"parent({parent_name}, {person1.lower()})")
            
            uncles_of_person1 = list(prolog.query(f"uncle(U, {person1.lower()})"))
            for uncle in uncles_of_person1:
                uncle_name = uncle["U"]
                prolog.assertz(f"uncle({uncle_name}, {person2.lower()})")

            aunts_of_person1 = list(prolog.query(f"aunt(A, {person1.lower()})"))
            for aunt in aunts_of_person1:
                aunt_name = aunt["A"]
                prolog.assertz(f"aunt({aunt_name}, {person2.lower()})")

           
            uncles_of_person2 = list(prolog.query(f"uncle(U, {person2.lower()})"))
            for uncle in uncles_of_person2:
                uncle_name = uncle["U"]
                prolog.assertz(f"uncle({uncle_name}, {person1.lower()})")

            aunts_of_person2 = list(prolog.query(f"aunt(A, {person2.lower()})"))
            for aunt in aunts_of_person2:
                aunt_name = aunt["A"]
                prolog.assertz(f"aunt({aunt_name}, {person1.lower()})")

       
            grandparents_of_person1 = list(prolog.query(f"grandparent(G, {person1.lower()})"))
            for grandparent in grandparents_of_person1:
                grandparent_name = grandparent["G"]
                if check_gender_compatibility(grandparent_name, 'male'):
                    prolog.assertz(f"grandfather({grandparent_name}, {person2.lower()})")
                elif check_gender_compatibility(grandparent_name, 'female'):
                    prolog.assertz(f"grandmother({grandparent_name}, {person2.lower()})")

            
            grandparents_of_person2 = list(prolog.query(f"grandparent(G, {person2.lower()})"))
            for grandparent in grandparents_of_person2:
                grandparent_name = grandparent["G"]
                if check_gender_compatibility(grandparent_name, 'male'):
                    prolog.assertz(f"grandfather({grandparent_name}, {person1.lower()})")
                elif check_gender_compatibility(grandparent_name, 'female'):
                    prolog.assertz(f"grandmother({grandparent_name}, {person1.lower()})")

            prolog.assertz(f"sibling({person1.lower()}, {person2.lower()})")
            return f"Learned that {person1} and {person2} are siblings."

        elif pattern_type == "father":
            father, child = args

            if is_parent_or_child(father, child):
                return f"{father} cannot be a father to {child} due to an existing parent/child relationship."

            if is_sibling(father, child):
                return f"{father} cannot be a father to {child} due to a sibling relationship."
            
            if is_aunt_uncle(father, child):
                return f"{father} cannot be a father to {child} due to an existing relationship."
            
            if is_grandparent(father, child):
                return f"{father} cannot be a father to {child} due to an existing relationship."

            if father.lower() == child.lower():
                return "A person cannot be their own father."
            
            if not check_gender_compatibility(father, 'male'):
                return f"{father} cannot be a father because they are not male."
            
            if check_for_circular_relationship(father, child):
                return f"A circular relationship cannot be established between {father} and {child}."
      
            if check_if_father_exists(child, father):
                return f"{child} already has a father."
            
            siblings = list(prolog.query(f"sibling(X, {child.lower()})"))
            for sibling in siblings:
                sibling_name = sibling["X"]
                if not check_if_father_exists(sibling_name, father):
                    prolog.assertz(f"parent({father.lower()}, {sibling_name})")

            prolog.assertz(f"parent({father.lower()}, {child.lower()})")
            prolog.assertz(f"male({father.lower()})")
            return f"Learned that {father} is the father of {child}."

        elif pattern_type == "mother":
            mother, child = args

            if is_parent_or_child(mother, child):
                return f"{mother} cannot be a mother to {child} due to an existing parent/child relationship."

            if is_sibling(mother, child):
                return f"{mother} cannot be a mother to {child} due to a sibling relationship."
            
            if is_aunt_uncle(mother, child):
                return f"{mother} cannot be a mother to {child} due to an existing relationship."
            
            if is_grandparent(mother, child):
                return f"{mother} cannot be a mother to {child} due to an existing relationship."

            if mother.lower() == child.lower():
                return "A person cannot be their own mother."

            if not check_gender_compatibility(mother, 'female'):
                return f"{mother} cannot be a mother because they are not female."
            
            if check_for_circular_relationship(mother, child):
                return f"A circular relationship cannot be established between {mother} and {child}."

            if check_if_mother_exists(child, mother):
                return f"{child} already has a mother."

            siblings = list(prolog.query(f"sibling(X, {child.lower()})"))
            for sibling in siblings:
                sibling_name = sibling["X"]
                if not check_if_mother_exists(sibling_name, mother):
                    prolog.assertz(f"parent({mother.lower()}, {sibling_name})")

            prolog.assertz(f"parent({mother.lower()}, {child.lower()})")
            prolog.assertz(f"female({mother.lower()})")
            return f"Learned that {mother} is the mother of {child}."

        elif pattern_type == "brother":
            brother, sibling = args

            if is_parent_or_child(brother, sibling):
                return f"{brother} cannot be a brother to {sibling} due to an existing parent/child relationship."

            if is_sibling(brother, sibling):
                return f"{brother} cannot be a brother to {sibling} due to a sibling relationship."
            
            if is_aunt_uncle(brother, sibling):
                return f"{brother} cannot be a brother to {sibling} due to an existing relationship."
            
            if is_grandparent(brother, sibling):
                return f"{brother} cannot be a brother to {sibling} due to an existing relationship."

            if not check_gender_compatibility(brother, 'male'):
                return f"{brother} cannot be a brother because they are not male."

            prolog.assertz(f"sibling({brother.lower()}, {sibling.lower()})")
            prolog.assertz(f"sibling({sibling.lower()}, {brother.lower()})")
            
    
            parents_of_sibling = list(prolog.query(f"parent(P, {sibling.lower()})"))
            for parent in parents_of_sibling:
                parent_name = parent["P"]
                prolog.assertz(f"parent({parent_name}, {brother.lower()})")

            parents_of_brother = list(prolog.query(f"parent(P, {brother.lower()})"))
            for parent in parents_of_brother:
                parent_name = parent["P"]
                prolog.assertz(f"parent({parent_name}, {sibling.lower()})")

            uncles_of_brother = list(prolog.query(f"uncle(U, {brother.lower()})"))
            for uncle in uncles_of_brother:
                uncle_name = uncle["U"]
                prolog.assertz(f"uncle({uncle_name}, {sibling.lower()})")

            aunts_of_brother = list(prolog.query(f"aunt(A, {brother.lower()})"))
            for aunt in aunts_of_brother:
                aunt_name = aunt["A"]
                prolog.assertz(f"aunt({aunt_name}, {sibling.lower()})")

            uncles_of_sibling = list(prolog.query(f"uncle(U, {sibling.lower()})"))
            for uncle in uncles_of_sibling:
                uncle_name = uncle["U"]
                prolog.assertz(f"uncle({uncle_name}, {brother.lower()})")

            aunts_of_sibling = list(prolog.query(f"aunt(A, {sibling.lower()})"))
            for aunt in aunts_of_sibling:
                aunt_name = aunt["A"]
                prolog.assertz(f"aunt({aunt_name}, {brother.lower()})")

            
            grandparents_of_brother = list(prolog.query(f"grandparent(G, {brother.lower()})"))
            for grandparent in grandparents_of_brother:
                grandparent_name = grandparent["G"]
                if check_gender_compatibility(grandparent_name, 'male'):
                    prolog.assertz(f"grandfather({grandparent_name}, {brother.lower()})")
                    prolog.assertz(f"grandfather({grandparent_name}, {sibling.lower()})")
                elif check_gender_compatibility(grandparent_name, 'female'):
                    prolog.assertz(f"grandmother({grandparent_name}, {brother.lower()})")
                    prolog.assertz(f"grandmother({grandparent_name}, {sibling.lower()})")

            grandparents_of_sibling = list(prolog.query(f"grandparent(G, {sibling.lower()})"))
            for grandparent in grandparents_of_sibling:
                grandparent_name = grandparent["G"]
                if check_gender_compatibility(grandparent_name, 'male'):
                    prolog.assertz(f"grandfather({grandparent_name}, {brother.lower()})")
                    prolog.assertz(f"grandfather({grandparent_name}, {sibling.lower()})")
                elif check_gender_compatibility(grandparent_name, 'female'):
                    prolog.assertz(f"grandmother({grandparent_name}, {brother.lower()})")
                    prolog.assertz(f"grandmother({grandparent_name}, {sibling.lower()})")

            prolog.assertz(f"male({brother.lower()})")
            return f"Learned that {brother} is a brother of {sibling}."

        elif pattern_type == "sister":
            sister, sibling = args

            if is_parent_or_child(sister, sibling):
                return f"{sister} cannot be a sister to {sibling} due to an existing parent/child relationship."

            if is_sibling(sister, sibling):
                return f"{sister} cannot be a sister to {sibling} due to a sibling relationship."
            
            if is_aunt_uncle(sister, sibling):
                return f"{sister} cannot be a sister to {sibling} due to an existing relationship."
            
            if is_grandparent(sister, sibling):
                return f"{sister} cannot be a sister to {sibling} due to an existing relationship."
            
            if not check_gender_compatibility(sister, 'female'):
                return f"{sister} cannot be a sister because they are not female."

            prolog.assertz(f"sibling({sister.lower()}, {sibling.lower()})")
            prolog.assertz(f"sibling({sibling.lower()}, {sister.lower()})")
            
            parents_of_sibling = list(prolog.query(f"parent(P, {sibling.lower()})"))
            for parent in parents_of_sibling:
                parent_name = parent["P"]
                prolog.assertz(f"parent({parent_name}, {sister.lower()})")

            parents_of_sister = list(prolog.query(f"parent(P, {sister.lower()})"))
            for parent in parents_of_sister:
                parent_name = parent["P"]
                prolog.assertz(f"parent({parent_name}, {sibling.lower()})")


            uncles_of_sister = list(prolog.query(f"uncle(U, {sister.lower()})"))
            for uncle in uncles_of_sister:
                uncle_name = uncle["U"]
                prolog.assertz(f"uncle({uncle_name}, {sibling.lower()})")

            aunts_of_sister = list(prolog.query(f"aunt(A, {sister.lower()})"))
            for aunt in aunts_of_sister:
                aunt_name = aunt["A"]
                prolog.assertz(f"aunt({aunt_name}, {sibling.lower()})")
      
            uncles_of_sibling = list(prolog.query(f"uncle(U, {sibling.lower()})"))
            for uncle in uncles_of_sibling:
                uncle_name = uncle["U"]
                prolog.assertz(f"uncle({uncle_name}, {sister.lower()})")

            aunts_of_sibling = list(prolog.query(f"aunt(A, {sibling.lower()})"))
            for aunt in aunts_of_sibling:
                aunt_name = aunt["A"]
                prolog.assertz(f"aunt({aunt_name}, {sister.lower()})")

            grandparents_of_sister = list(prolog.query(f"grandparent(G, {sister.lower()})"))
            for grandparent in grandparents_of_sister:
                grandparent_name = grandparent["G"]
                if check_gender_compatibility(grandparent_name, 'male'):
                    prolog.assertz(f"grandfather({grandparent_name}, {sister.lower()})")
                    prolog.assertz(f"grandfather({grandparent_name}, {sibling.lower()})")
                elif check_gender_compatibility(grandparent_name, 'female'):
                    prolog.assertz(f"grandmother({grandparent_name}, {sister.lower()})")
                    prolog.assertz(f"grandmother({grandparent_name}, {sibling.lower()})")

            grandparents_of_sibling = list(prolog.query(f"grandparent(G, {sibling.lower()})"))
            for grandparent in grandparents_of_sibling:
                grandparent_name = grandparent["G"]
                if check_gender_compatibility(grandparent_name, 'male'):
                    prolog.assertz(f"grandfather({grandparent_name}, {sister.lower()})")
                    prolog.assertz(f"grandfather({grandparent_name}, {sibling.lower()})")
                elif check_gender_compatibility(grandparent_name, 'female'):
                    prolog.assertz(f"grandmother({grandparent_name}, {sister.lower()})")
                    prolog.assertz(f"grandmother({grandparent_name}, {sibling.lower()})")
            

            prolog.assertz(f"female({sister.lower()})")
            return f"Learned that {sister} is a sister of {sibling}."

        elif pattern_type == "grandfather":
            grandfather, grandchild = args

            if is_parent_or_child(grandfather, grandchild):
                return f"{grandfather} cannot be a grandfather to {grandchild} due to an existing parent/child relationship."

            if is_sibling(grandfather, grandchild):
                return f"{grandfather} cannot be a grandfather to {grandchild} due to a sibling relationship."
            
            if is_aunt_uncle(grandfather, grandchild):
                return f"{grandfather} cannot be a grandfather to {grandchild} due to an existing relationship."
            
            if is_grandparent(grandfather, grandchild):
                return f"{grandfather} cannot be a grandfather to {grandchild} due to an existing relationship."
   
            if not check_gender_compatibility(grandfather, 'male'):
                return f"{grandfather} cannot be a grandfather because they are not male."
            
            siblings = list(prolog.query(f"sibling(X, {grandchild.lower()})"))
            for sibling in siblings:
                sibling_name = sibling["X"]
                prolog.assertz(f"grandfather({grandfather.lower()}, {sibling_name})")
            
            prolog.assertz(f"grandparent({grandfather.lower()}, {grandchild.lower()})")
            prolog.assertz(f"grandfather({grandfather.lower()}, {grandchild.lower()})")
            return f"Learned that {grandfather} is the grandfather of {grandchild}."

        elif pattern_type == "grandmother":
            grandmother, grandchild = args

            if is_parent_or_child(grandmother, grandchild):
                return f"{grandmother} cannot be a grandmother to {grandchild} due to an existing parent/child relationship."

            if is_sibling(grandmother, grandchild):
                return f"{grandmother} cannot be a grandmother to {grandchild} due to a sibling relationship."
            
            if is_aunt_uncle(grandmother, grandchild):
                return f"{grandmother} cannot be a grandmother to {grandchild} due to an existing relationship."
            
            if is_grandparent(grandmother, grandchild):
                return f"{grandmother} cannot be a grandmother to {grandchild} due to an existing relationship."
         
            if not check_gender_compatibility(grandmother, 'female'):
                return f"{grandmother} cannot be a grandmother because they are not female."
            
            siblings = list(prolog.query(f"sibling(X, {grandchild.lower()})"))
            for sibling in siblings:
                sibling_name = sibling["X"]
                prolog.assertz(f"grandmother({grandmother.lower()}, {sibling_name})")
            
            prolog.assertz(f"grandparent({grandmother.lower()}, {grandchild.lower()})")
            prolog.assertz(f"grandmother({grandmother.lower()}, {grandchild.lower()})")
            return f"Learned that {grandmother} is the grandmother of {grandchild}."

        elif pattern_type == "child":
            child, parent = args

            if child.lower() == parent.lower():
                return "A person cannot be their own child."
            
            if is_parent_or_child(parent, child):
                return f"{parent} cannot be a parent to {child} due to an existing parent/child relationship."

            if is_sibling(parent, child):
                return f"{parent} cannot be a parent to {child} due to a sibling relationship."
            
            if is_aunt_uncle(parent, child):
                return f"{parent} cannot be a parent to {child} due to an existing relationship."
            
            if is_grandparent(parent, child):
                return f"{parent} cannot be a parent to {child} due to an existing relationship."
            
            existing_parent = existing_parents(child)
            if existing_parent == "mother":
                prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                prolog.assertz(f"father({parent.lower()}, {child.lower()})")  
                return f"Learned that {parent} is the father of {child}."
            elif existing_parent == "father":
                prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                prolog.assertz(f"mother({parent.lower()}, {child.lower()})")  
                return f"Learned that {parent} is the mother of {child}."

            prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
            return f"Learned that {child} is a child of {parent}."

        elif pattern_type == "son":
            son, parent = args

            if son.lower() == parent.lower():
                return "A person cannot be their own son."
            
            if is_parent_or_child(parent, son):
                return f"{parent} cannot be a parent to {son} due to an existing parent/child relationship."

            if is_sibling(parent, son):
                return f"{parent} cannot be a parent to {son} due to a sibling relationship."
            
            if is_aunt_uncle(parent, son):
                return f"{parent} cannot be a parent to {son} due to an existing relationship."
            
            if is_grandparent(parent, son):
                return f"{parent} cannot be a parent to {son} due to an existing relationship."

            if not check_gender_compatibility(son, 'male'):
                return f"{son} cannot be a son because they are not male."
            
            existing_parent = existing_parents(son)
            if existing_parent == "mother":
                prolog.assertz(f"parent({parent.lower()}, {son.lower()})")
                prolog.assertz(f"father({parent.lower()}, {son.lower()})")  
                return f"Learned that {parent} is the father of {son}."
            elif existing_parent == "father":
                prolog.assertz(f"parent({parent.lower()}, {son.lower()})")
                prolog.assertz(f"mother({parent.lower()}, {son.lower()})")  
                return f"Learned that {parent} is the mother of {son}."

            prolog.assertz(f"parent({parent.lower()}, {son.lower()})")
            prolog.assertz(f"male({son.lower()})")
            return f"Learned that {son} is a son of {parent}."

        elif pattern_type == "daughter":
            daughter, parent = args

            if daughter.lower() == parent.lower():
                return "A person cannot be their own daughter."
            
            if is_parent_or_child(parent, daughter):
                return f"{parent} cannot be a parent to {daughter} due to an existing parent/child relationship."

            if is_sibling(parent, daughter):
                return f"{parent} cannot be a parent to {daughter} due to a sibling relationship."
            
            if is_aunt_uncle(parent, daughter):
                return f"{parent} cannot be a parent to {daughter} due to an existing relationship."
            
            if is_grandparent(parent, daughter):
                return f"{parent} cannot be a parent to {daughter} due to an existing relationship."
            
            if not check_gender_compatibility(daughter, 'female'):
                return f"{daughter} cannot be a daughter because they are not female."
            
            existing_parent = existing_parents(daughter)
            if existing_parent == "mother":
                prolog.assertz(f"parent({parent.lower()}, {daughter.lower()})")
                prolog.assertz(f"father({parent.lower()}, {daughter.lower()})")  
                return f"Learned that {parent} is the father of {daughter}."
            elif existing_parent == "father":
                prolog.assertz(f"parent({parent.lower()}, {daughter.lower()})")
                prolog.assertz(f"mother({parent.lower()}, {daughter.lower()})")  
                return f"Learned that {parent} is the mother of {daughter}."

            prolog.assertz(f"parent({parent.lower()}, {daughter.lower()})")
            prolog.assertz(f"female({daughter.lower()})")
            return f"Learned that {daughter} is a daughter of {parent}."

        elif pattern_type == "uncle":
            uncle, nephew_niece = args


            if not check_gender_compatibility(uncle, 'male'):
                return f"{uncle} cannot be an uncle because they are not male."
            
            if is_parent_or_child(uncle, nephew_niece):
                return f"{uncle} cannot be an uncle to {nephew_niece} due to an existing parent/child relationship."

            if is_sibling(uncle, nephew_niece):
                return f"{uncle} cannot be an uncle to {nephew_niece} due to a sibling relationship."
            
            if is_aunt_uncle(uncle, nephew_niece):
                return f"{uncle} cannot be an uncle to {nephew_niece} due to an existing relationship."
            
            if is_grandparent(uncle, nephew_niece):
                return f"{uncle} cannot be an uncle to {nephew_niece} due to an existing relationship."
            
            siblings = list(prolog.query(f"sibling(X, {nephew_niece.lower()})"))
            for sibling in siblings:
                sibling_name = sibling["X"]
                prolog.assertz(f"uncle({uncle.lower()}, {sibling_name.lower()})")
            
            prolog.assertz(f"uncle({uncle.lower()}, {nephew_niece.lower()})")
            prolog.assertz(f"male({uncle.lower()})")
            return f"Learned that {uncle} is an uncle of {nephew_niece}."

        elif pattern_type == "aunt":
            aunt, nephew_niece = args

            if is_parent_or_child(aunt, nephew_niece):
                return f"{aunt} cannot be an aunt to {nephew_niece} due to an existing parent/child relationship."

            if is_sibling(aunt, nephew_niece):
                return f"{aunt} cannot be an aunt to {nephew_niece} due to a sibling relationship."
            
            if is_aunt_uncle(aunt, nephew_niece):
                return f"{aunt} cannot be an aunt to {nephew_niece} due to an existing relationship."
            
            if is_grandparent(aunt, nephew_niece):
                return f"{aunt} cannot be an aunt to {nephew_niece} due to an existing relationship."

          
            if not check_gender_compatibility(aunt, 'female'):
                return f"{aunt} cannot be an aunt because they are not female."
            
            siblings = list(prolog.query(f"sibling(X, {nephew_niece.lower()})"))
            for sibling in siblings:
                sibling_name = sibling["X"]
                prolog.assertz(f"aunt({aunt.lower()}, {sibling_name.lower()})")

            prolog.assertz(f"aunt({aunt.lower()}, {nephew_niece.lower()})")
            prolog.assertz(f"female({aunt.lower()})")
            return f"Learned that {aunt} is an aunt of {nephew_niece}."

        elif pattern_type == "parents":
            parent1, parent2, child = args

            if is_parent_or_child(parent1, child):
                return f"{parent1} cannot be a parent to {child} due to an existing parent/child relationship."
            
            if is_parent_or_child(parent2, child):
                return f"{parent2} cannot be a parent to {child} due to an existing parent/child relationship."

            if is_sibling(parent1, child):
                return f"{parent1} cannot be a parent to {child} due to a sibling relationship."
            
            if is_sibling(parent2, child):
                return f"{parent2} cannot be a parent to {child} due to an sibling relationship."

            if is_aunt_uncle(parent1, child):
                return f"{parent1} cannot be an parent to {child} due to an existing relationship."
            
            if is_grandparent(parent1, child):
                return f"{parent1} cannot be an parent to {child} due to an existing relationship."
            
            if is_aunt_uncle(parent2, child):
                return f"{parent2} cannot be an parent to {child} due to an existing relationship."
            
            if is_grandparent(parent2, child):
                return f"{parent2} cannot be an parent to {child} due to an existing relationship."

            if parent1.lower() == child.lower() or parent2.lower() == child.lower():
                return "A person cannot be their own parent."

            if check_multiple_parents(child):
                return f"{child} already has a mother and/or a father, and additional parents cannot be added."
        
            siblings = list(prolog.query(f"sibling(X, {child.lower()})"))
            for sibling in siblings:
                sibling_name = sibling["X"]
                if not check_if_parent_exists(sibling_name, parent1):
                    prolog.assertz(f"parent({parent1.lower()}, {sibling_name})")
                if not check_if_parent_exists(sibling_name, parent2):
                    prolog.assertz(f"parent({parent2.lower()}, {sibling_name})")
            
            
            prolog.assertz(f"parent({parent1.lower()}, {child.lower()})")
            prolog.assertz(f"parent({parent2.lower()}, {child.lower()})")

            return f"Learned that {parent1} and {parent2} are the parents of {child}."
        

        elif pattern_type == "children":
            child1, child2, child3, parent = args

           
            for child in [child1, child2, child3]:
                if is_parent_or_child(parent, child):
                    return f"{parent} cannot be a parent to {child} due to an existing parent/child relationship."

                if is_sibling(parent, child):
                    return f"{parent} cannot be a parent to {child} due to a sibling relationship."
                
                if is_aunt_uncle(parent, child):
                    return f"{parent} cannot be a parent to {child} due to an existing relationship."
                
                if is_grandparent(parent, child):
                    return f"{parent} cannot be a parent to {child} due to an existing relationship."
                
                if child.lower() == parent.lower():
                    return "A person cannot be their own parent."

         
            for child in [child1, child2, child3]:
                existing_parent = existing_parents(child)
                if existing_parent == "mother":
                    prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                    prolog.assertz(f"father({parent.lower()}, {child.lower()})")  
                    return f"Learned that {parent} is the father of {child}."
                elif existing_parent == "father":
                    prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
                    prolog.assertz(f"mother({parent.lower()}, {child.lower()})")  
                    return f"Learned that {parent} is the mother of {child}."
            
            
            for child in [child1, child2, child3]:
                prolog.assertz(f"parent({parent.lower()}, {child.lower()})")

            return f"Learned that {child1}, {child2}, and {child3} are children of {parent}."

        return "I couldn't understand that statement."
    
    except Exception as e:
        return "That’s impossible!"





def process_question(pattern_type, args):
    try:
       
        if pattern_type.startswith("Who"):
            relation = pattern_type.split(" ")[-1].replace("Who", "").replace("_q", "").strip()
            person = args[0].lower()
            
            if relation == "siblings":
                query = f"sibling(X, {person})"
            elif relation == "sisters":
                query = f"sister(X, {person})"
            elif relation == "brothers":
                query = f"brother(X, {person})"
            elif relation == "mother":
                query = f"mother(X, {person})"
            elif relation == "father":
                query = f"father(X, {person})"
            elif relation == "parents":
                query = f"parent(X, {person})"
            elif relation == "daughters":
                query = f"daughter(X, {person})"
            elif relation == "sons":
                query = f"son(X, {person})"
            elif relation == "children":
                query = f"child(X, {person})"
            else:
                return "I couldn't process that question."

            results = list(prolog.query(query))

            if results:
              
                answers = [result["X"] for result in results]

                unique_answers = list(set(answers))

                if len(unique_answers) == 1:
                    return f"The {relation} of {args[0]} is {unique_answers[0]}."
                else:
                    return f"The {relation} of {args[0]} are {', '.join(unique_answers)}."
            else:
                return f"No {relation} found for {args[0]}."

       
        elif pattern_type.endswith("_q"):  
            relation = pattern_type.replace("_q", "")
            query = build_prolog_query(relation, args)
            result = list(prolog.query(query))
            return "Yes" if result else "No"

        return "I couldn't process that question."

    except Exception as e:
        return f"An error occurred: {e}"


def build_prolog_query(relation, args, find_all=False):
    
    if relation == "siblings":
        if find_all:
            return f"sibling(X, {args[0].lower()})"
        else:
            return f"sibling({args[0].lower()}, {args[1].lower()})"

    elif relation == "brother":
        if find_all:
            return f"brother(X, {args[0].lower()})"
        else:
            return f"brother({args[0].lower()}, {args[1].lower()})"

    elif relation == "sister":
        if find_all:
            return f"sister(X, {args[0].lower()})"
        else:
            return f"sister({args[0].lower()}, {args[1].lower()})"

    elif relation == "father":
        if find_all:
            return f"father(X, {args[0].lower()})"
        else:
            return f"father({args[0].lower()}, {args[1].lower()})"

    elif relation == "mother":
        if find_all:
            return f"mother(X, {args[0].lower()})"
        else:
            return f"mother({args[0].lower()}, {args[1].lower()})"

    elif relation == "grandfather":
        if find_all:
            return f"grandfather(X, {args[0].lower()})"
        else:
            return f"grandfather({args[0].lower()}, {args[1].lower()})"

    elif relation == "grandmother":
        if find_all:
            return f"grandmother(X, {args[0].lower()})"
        else:
            return f"grandmother({args[0].lower()}, {args[1].lower()})"

    elif relation == "parents":
        if find_all:
            return f"parent(X, {args[0].lower()})"
        else:
            return f"parent({args[0].lower()}, {args[1].lower()})"

    elif relation == "children":
        if find_all:
            return f"child(X, {args[0].lower()})"
        else:
            return f"child({args[0].lower()}, {args[1].lower()})"
        
    elif relation == "child":
        if find_all:
            return f"child(X, {args[0].lower()})"
        else:
            return f"child({args[0].lower()}, {args[1].lower()})"

    elif relation == "son":
        if find_all:
            return f"son(X, {args[0].lower()})"
        else:
            return f"son({args[0].lower()}, {args[1].lower()})"

    elif relation == "daughter":
        if find_all:
            return f"daughter(X, {args[0].lower()})"
        else:
            return f"daughter({args[0].lower()}, {args[1].lower()})"

    elif relation == "uncle":
        if find_all:
            return f"uncle(X, {args[0].lower()})"
        else:
            return f"uncle({args[0].lower()}, {args[1].lower()})"

    elif relation == "aunt":
        if find_all:
            return f"aunt(X, {args[0].lower()})"
        else:
            return f"aunt({args[0].lower()}, {args[1].lower()})"

    elif relation == "relatives":
        if find_all:
            return f"relatives(X, {args[0].lower()})"
        else:
            return f"relatives({args[0].lower()}, {args[1].lower()})"

    return ""


def chatbot():
    print("Welcome to the Family Relationship Chatbot!")
    print("Type 'exit' to leave the chat.")
    
    while True:
        user_input = input("Enter a statement or question: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        
        pattern_type, args = match_pattern(user_input)
        if not pattern_type:
            print("Sorry, I didn't understand that.")
            continue

        if pattern_type.endswith("_q"):
            response = process_question(pattern_type, args)
        else:  
            response = process_statement(pattern_type, args)
        
        print(response)


if __name__ == "__main__":
    chatbot()
