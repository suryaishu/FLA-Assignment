def epsilon_closure(states, transitions):
    epsilon_states = set(states)
    stack = list(states)

    while stack:
        current_state = stack.pop()
        if current_state in transitions and 'ε' in transitions[current_state]:
            for next_state in transitions[current_state]['ε']:
                if next_state not in epsilon_states:
                    epsilon_states.add(next_state)
                    stack.append(next_state)

    return epsilon_states

def move(states, symbol, transitions):
    move_states = set()
    for state in states:
        if state in transitions and symbol in transitions[state]:
            move_states.update(transitions[state][symbol])
    return move_states

def epsilon_nfa_to_nfa(epsilon_nfa):
    nfa = {
        'states': set(),
        'alphabet': epsilon_nfa['alphabet'],
        'transitions': {},
        'start_state': epsilon_nfa['start_state'],
        'accept_states': epsilon_nfa['accept_states']
    }

    stack = [epsilon_nfa['start_state']]
    nfa['states'].add(epsilon_nfa['start_state'])

    while stack:
        current_state = stack.pop()
        epsilon_states = epsilon_closure({current_state}, epsilon_nfa['transitions'])

        for symbol in nfa['alphabet']:
            move_states = epsilon_closure(move(epsilon_states, symbol, epsilon_nfa['transitions']), epsilon_nfa['transitions'])

            if move_states:
                state_str = ''.join(sorted(list(move_states)))
                nfa['transitions'].setdefault(current_state, {})[symbol] = state_str

                if state_str not in nfa['states']:
                    nfa['states'].add(state_str)
                    stack.append(state_str)

    return nfa

# Input your ε-NFA here
epsilon_nfa = {
    'alphabet': {'0', '1'},
    'transitions': {
        'q0': {'ε': {'q1'}},
        'q1': {'0': {'q1'}, 'ε': {'q2'}},
        'q2': {'1': {'q3'}},
        'q3': {'0': {'q3'}, '1': {'q3'}}
    },
    'start_state': 'q0',
    'accept_states': {'q3'}
}

nfa_result = epsilon_nfa_to_nfa(epsilon_nfa)
print("NFA Result:")
print(nfa_result)

# Test the NFA with an input string
input_str = input("Enter an input string: ")
current_state = nfa_result['start_state']

for symbol in input_str:
    if symbol not in nfa_result['alphabet']:
        print("Invalid input symbol.")
        break
    if current_state in nfa_result['transitions'] and symbol in nfa_result['transitions'][current_state]:
        current_state = nfa_result['transitions'][current_state][symbol]
    else:
        print("Input string not accepted.")
        break
else:
    if current_state in nfa_result['accept_states']:
        print("Input string accepted.")
    else:
        print("Input string not accepted.")
