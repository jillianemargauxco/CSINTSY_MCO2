import re
from pyswip import Prolog

# Initialize Prolog engine
prolog = Prolog()
prolog.consult("family.pl")  # Load the Prolog knowledge base


def match_pattern(user_input):
    """Match user input to a defined statement or question pattern."""
   
    patterns = {
       
        "siblings": r"(.+) and (.+) are siblings",
        "brother": r"(.+) is a brother of (.+)",
        "sister": r"(.+) is a sister of (.+)",
        "father": r"(.+) is the father of (.+)",
        "mother": r"(.+) is the mother of (.+)",
        "parents": r"(.+) and (.+) are the parents of (.+)",

        "grandmother": r"(.+) is a grandmother of (.+)",
        "grandfather": r"(.+) is a grandfather of (.+)",
        "child": r"(.+) is a child of (.+)",
        "children": r"(.+) and (.+) are children of (.+)",
        "daughter": r"(.+) is a daughter of (.+)",
        "son": r"(.+) is a son of (.+)",
        "uncle": r"(.+) is an uncle of (.+)",
        "aunt": r"(.+) is an aunt of (.+)",
        

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


def process_statement(pattern_type, args):
    """Process statements and assert them into the Prolog knowledge base."""
    try:
        if pattern_type == "siblings":
            person1, person2 = args
            prolog.assertz(f"sibling({person1.lower()}, {person2.lower()})")
            prolog.assertz(f"sibling({person2.lower()}, {person1.lower()})")  # Sibling is symmetric
            return f"Learned that {person1} and {person2} are siblings."

        elif pattern_type == "father":
            father, child = args
            prolog.assertz(f"parent({father.lower()}, {child.lower()})")
            prolog.assertz(f"male({father.lower()})")
            return f"Learned that {father} is the father of {child}."

        elif pattern_type == "mother":
            mother, child = args
            prolog.assertz(f"parent({mother.lower()}, {child.lower()})")
            prolog.assertz(f"female({mother.lower()})")
            return f"Learned that {mother} is the mother of {child}."

        elif pattern_type == "grandfather":
            grandfather, grandchild = args
            prolog.assertz(f"grandfather({grandfather.lower()}, {grandchild.lower()})")
            prolog.assertz(f"male({grandfather.lower()})")
            return f"Learned that {grandfather} is the grandfather of {grandchild}."

        elif pattern_type == "grandmother":
            grandmother, grandchild = args
            prolog.assertz(f"grandmother({grandmother.lower()}, {grandchild.lower()})")
            prolog.assertz(f"female({grandmother.lower()})")
            return f"Learned that {grandmother} is the grandmother of {grandchild}."

        elif pattern_type == "child":
            child, parent = args
            prolog.assertz(f"parent({parent.lower()}, {child.lower()})")
            return f"Learned that {child} is a child of {parent}."

        elif pattern_type == "son":
            son, parent = args
            prolog.assertz(f"parent({parent.lower()}, {son.lower()})")
            prolog.assertz(f"male({son.lower()})")
            return f"Learned that {son} is a son of {parent}."

        elif pattern_type == "daughter":
            daughter, parent = args
            prolog.assertz(f"parent({parent.lower()}, {daughter.lower()})")
            prolog.assertz(f"female({daughter.lower()})")
            return f"Learned that {daughter} is a daughter of {parent}."

        elif pattern_type == "uncle":
            uncle, nephew_niece = args
            prolog.assertz(f"uncle({uncle.lower()}, {nephew_niece.lower()})")
            prolog.assertz(f"male({uncle.lower()})")
            return f"Learned that {uncle} is an uncle of {nephew_niece}."

        elif pattern_type == "aunt":
            aunt, nephew_niece = args
            prolog.assertz(f"aunt({aunt.lower()}, {nephew_niece.lower()})")
            prolog.assertz(f"female({aunt.lower()})")
            return f"Learned that {aunt} is an aunt of {nephew_niece}."

        elif pattern_type == "parents":
            parent1, parent2, child = args
            prolog.assertz(f"parent({parent1.lower()}, {child.lower()})")
            prolog.assertz(f"parent({parent2.lower()}, {child.lower()})")
            return f"Learned that {parent1} and {parent2} are the parents of {child}."

        elif pattern_type == "children":
            child1, child2, parent = args
            prolog.assertz(f"parent({parent.lower()}, {child1.lower()})")
            prolog.assertz(f"parent({parent.lower()}, {child2.lower()})")
            return f"Learned that {child1} and {child2} are children of {parent}."

        elif pattern_type == "relatives":
            person1, person2 = args
            prolog.assertz(f"relatives({person1.lower()}, {person2.lower()})")
            prolog.assertz(f"relatives({person2.lower()}, {person1.lower()})")  
            return f"Learned that {person1} and {person2} are relatives."

        return "I couldn't understand that statement."

    except Exception as e:
        print(f"Error: {e}")
        return "That’s impossible!"




def process_question(pattern_type, args):
    """Process a question by querying the Prolog knowledge base."""
    try:
        if pattern_type.endswith("_q"):  # Yes/No Questions
            relation = pattern_type.replace("_q", "")
            query = build_prolog_query(relation, args)
            result = list(prolog.query(query))
            return "yes" if result else "no"

        elif pattern_type.startswith("Who"):  # Who/What Questions
            relation = pattern_type.replace("_q", "")
            query = build_prolog_query(relation, args, find_all=True)
            results = list(prolog.query(query))
            if results:
                answers = [r["X"] for r in results]
                return f"The {relation} of {args[0]} are: {', '.join(answers)}."
            return f"I couldn't find any {relation} for {args[0]}."

    except Exception:
        return "That’s impossible!"

def build_prolog_query(relation, args, find_all=False):
    """Generate a Prolog query based on the relationship and arguments."""
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
    """Main chatbot loop."""
    print("Welcome to the Intelligent Family Relationship Chatbot!")
    print("Type 'exit' to leave the chat.")
    
    while True:
        user_input = input("Enter a statement or question: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Match the user input to a pattern
        pattern_type, args = match_pattern(user_input)
        if not pattern_type:
            print("Sorry, I didn't understand that.")
            continue

        if pattern_type.endswith("_q"):  # Question
            response = process_question(pattern_type, args)
        else:  # Statement
            response = process_statement(pattern_type, args)
        
        print(response)


if __name__ == "__main__":
    chatbot()
