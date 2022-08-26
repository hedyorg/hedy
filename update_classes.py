from website import dynamo

# Make sure we add the correct env variables
storage = dynamo.AwsDynamoStorage.from_env()
if not storage:
    print("Something went wrong with connecting to the AWS database...")
    exit(1)

# Get the correct tables
USERS = dynamo.Table(storage, 'users', 'username', indexed_fields=[dynamo.IndexKey('email')])
CLASSES = dynamo.Table(storage, 'classes', 'id', indexed_fields=[dynamo.IndexKey(v) for v in ['teacher', 'link']])

# Get all classes
classes = CLASSES.scan()
teacher_classes = {}

# For each class -> change "teacher string" into "teachers set"
for Class in classes:
    CLASSES.update({'id': Class.get('id')}, {'teacher': None, 'teachers': {Class.get('teacher')}})
    if not teacher_classes.get(Class.get('teacher')):
        teacher_classes[Class.get('teacher')] = set()
    teacher_classes[Class.get('teacher')].add(Class.get('id'))

# Add "teacher_classes" to each user
for teacher, classes in teacher_classes.items():
    USERS.update({'username': teacher}, {'teacher_classes': classes})