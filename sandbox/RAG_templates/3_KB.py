import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from code_kb import CodeKnowledgeBase
from index_codebase import index_codebase
from code_rag import CodeRAG

print("Initializing system...")
kb = CodeKnowledgeBase("understand_test")
index_codebase(kb)
rag = CodeRAG(kb)

# Test understanding various code snippets
test_cases = [
    {
        'name': 'Registration Function',
        'code': """def register_new_user(username, email, pwd):
    '''Register new user in system.'''
    if '@' not in email:
        return {'error': 'Invalid email'}
    if len(pwd) < 8:
        return {'error': 'Password too short'}
    
    import hashlib
    hashed = hashlib.sha256(pwd.encode()).hexdigest()
    
    user_data = {
        'username': username,
        'email': email,
        'password': hashed
    }
    
    return user_data"""
    },
    {
        'name': 'Session Check',
        'code': """def verify_user_session(token):
    sessions = get_active_sessions()
    for sess in sessions:
        if sess['token'] == token and sess['expires'] > now():
            return sess['user_id']
    return None"""
    },
]

print("\n" + "="*60)
print("Code Understanding Tests")
print("="*60)

for test in test_cases:
    print(f"\n\n{'='*60}")
    print(f"Test: {test['name']}")
    print("="*60)
    print(f"\nCode:\n{test['code']}\n")
    print("-" * 60)
    
    result = rag.explain_code(test['code'])
    
    print("Explanation:")
    print(result['explanation'])
    
    print("\n\nSimilar functions in codebase:")
    for func in result['similar_functions']:
        meta = func['metadata']
        print(f"\n  - {meta['name']} (distance: {func['distance']:.3f})")
        print(f"    {meta['docstring']}")