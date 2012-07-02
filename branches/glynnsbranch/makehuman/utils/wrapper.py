# -*- coding: utf-8 -*-
from string import Template

method_declaration = Template('static PyObject *${classname}_${methodname}(${classname} *self${parameter});\n')

methods_begin = ''\
'// ${classname} Methods\n'\
'static PyMethodDef ${classname}_methods[] =\n'\
'{\n'
method = Template(''\
'    {"${methodname}", (PyCFunction)${classname}_${methodname}, METH_VARARGS, "${comment}"},\n')
methods_end = ''\
'    {NULL}  /* Sentinel */\n'\
'};\n'

argument = {'METH_VARARGS':', PyObject *args', 'METH_O':', PyObject *arg', 'METH_NOARGS':''}

def writeMethods(c):
    for m in c['methods']:
        print(method_declaration.substitute(classname = c['name'], methodname=m['name'], parameter=argument[m['type']]));
    methods = methods_begin
    for m in c['methods']:
        methods += method.safe_substitute(methodname=m['name'], comment=m['comment'])
    methods += methods_end
    methods = Template(methods)
    print(methods.substitute(classname = c['name']));

members_begin = ''\
'// ${classname} Members\n'\
'static PyMemberDef ${classname}_members[] =\n'\
'{\n'
member = Template(''\
'    {"${membername}", ${membertype}, offsetof(${classname}, ${membername}), 0, "${comment}"},\n')
members_end = ''\
'    {NULL}  /* Sentinel */\n'\
'};\n'

def writeMembers(c):
    members = members_begin
    for m in c['members']:
        members += member.safe_substitute(membername=m['name'], membertype=m['type'], comment=m['comment'])
    members += members_end
    members = Template(members)
    print(members.substitute(classname = c['name']));

properties_begin = ''\
'// ${classname} Properties\n'\
'static PyGetSetDef ${classname}_getset[] =\n'\
'{\n'
property = Template(''\
'    {"${propertyname}", (getter)${classname}_get${propertyname}, (setter)${classname}_set${propertyname}, "${comment}", NULL},\n')
properties_end = ''\
'    {NULL}  /* Sentinel */\n'\
'};\n'

def writeProperties(c):
    properties = properties_begin
    for m in c['properties']:
        properties += property.safe_substitute(propertyname=m['name'], comment='')
    properties += methods_end
    properties = Template(properties)
    print(properties.substitute(classname = c['name']));
    
new_declaration = Template('static PyObject *${classname}_new(PyTypeObject *type, PyObject *args, PyObject *kwds);\n')

def writeNewDeclaration(c):
    print(new_declaration.substitute(classname = c['name']));
    
init_declaration = Template('static PyObject *${classname}_init(${classname} *self, PyObject *args, PyObject *kwds);\n')

def writeInitDeclaration(c):
    print(init_declaration.substitute(classname = c['name']));
    
dealloc_declaration = Template('static void ${classname}_dealloc(${classname} *self);\n')

def writeDeallocDeclaration(c):
    print(dealloc_declaration.substitute(classname = c['name']));
        
type = Template(''\
'// ${classname} type definition\n'\
'PyTypeObject ${classname}Type =\n'\
'{\n'\
'    PyObject_HEAD_INIT(NULL)\n'\
'    0,                                        // ob_size\n'\
'    "${modulename}.${classname}",             // tp_name\n'\
'    sizeof(${classname}),                     // tp_basicsize\n'\
'    0,                                        // tp_itemsize\n'\
'    ${dealloc},                               // tp_dealloc\n'\
'    0,                                        // tp_print\n'\
'    0,                                        // tp_getattr\n'\
'    0,                                        // tp_setattr\n'\
'    0,                                        // tp_compare\n'\
'    0,                                        // tp_repr\n'\
'    0,                                        // tp_as_number\n'\
'    0,                                        // tp_as_sequence\n'\
'    0,                                        // tp_as_mapping\n'\
'    0,                                        // tp_hash\n'\
'    0,                                        // tp_call\n'\
'    0,                                        // tp_str\n'\
'    0,                                        // tp_getattro\n'\
'    0,                                        // tp_setattro\n'\
'    0,                                        // tp_as_buffer\n'\
'    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, // tp_flags\n'\
'    "${classname} object",                    // tp_doc\n'\
'    0,                                        // tp_traverse\n'\
'    0,                                        // tp_clear\n'\
'    0,                                        // tp_richcompare\n'\
'    0,                                        // tp_weaklistoffset\n'\
'    0,                                        // tp_iter\n'\
'    0,                                        // tp_iternext\n'\
'    $methods,                                 // tp_methods\n'\
'    $members,                                 // tp_members\n'\
'    $getset,                                  // tp_getset\n'\
'    0,                                        // tp_base\n'\
'    0,                                        // tp_dict\n'\
'    0,                                        // tp_descr_get\n'\
'    0,                                        // tp_descr_set\n'\
'    0,                                        // tp_dictoffset\n'\
'    ${init},                                  // tp_init\n'\
'    0,                                        // tp_alloc\n'\
'    ${new},                                   // tp_new\n'\
'};\n')

def writeType(c):
    methods = '${classname}_methods' if c['methods'] else "0"
    members = '${classname}_members' if c['members'] else "0"
    properties = '${classname}_properties' if c['properties'] else "0"
    new = '${classname}_new' if "new" in c else "0"
    init = '(initproc)${classname}_init' if "init" in c else "0"
    dealloc = '(destructor)${classname}_dealloc' if "dealloc" in c else "0"
    templ = Template(type.safe_substitute(methods = methods, members = members, getset = properties, new = new, init = init, dealloc = dealloc))
    print(templ.substitute(modulename = c['module'], classname = c['name']));
    
register = Template(''\
'void Register${classname}(PyObject *module)\n'\
'{\n'\
'    if (PyType_Ready(&${classname}Type) < 0)\n'\
'        return;\n'\
'\n'\
'    Py_INCREF(&${classname}Type);\n'\
'    PyModule_AddObject(module, "${classname}", (PyObject*)&${classname}Type);\n'\
'}\n')

def writeRegister(c):
    print(register.substitute(classname = c['name']));
    
def writeClass(c):
    if c['methods']:
        writeMethods(c)
    if c['members']:
        writeMembers(c)
    if c['properties']:
        writeProperties(c)
    if 'new' in c:
        writeNewDeclaration(c)
    if 'init' in c:
        writeInitDeclaration(c)
    if 'dealloc' in c:
        writeDeallocDeclaration(c)
    writeType(c)
    writeRegister(c)
    
modulename = 'untitled_module'
classes = []

types={'float':'T_FLOAT','uint':'T_UINT'}
method_types={'varargs':'METH_VARARGS','object':'METH_O'}

with open('mh.desc', 'rb') as f:
    c = {}
    for line in f:
        if line.startswith('module'):
            modulename = line.split()[1]
        if line.startswith('class'):
            c = {'methods':[], 'members':[], 'properties':[]}
            c['name'] = line.split()[1]
            c['module'] = modulename
            classes.append(c)
        elif line.startswith('method'):
            m = {'name':line.split()[1], 'type':method_types[line.split()[2]]}
            if len(line.split()) > 3:
                m['comment'] = ' '.join(line.split()[3:])
            else:
                m['comment'] = ""
            c['methods'].append(m)
        elif line.startswith('member'):
            m = {'type':types[line.split()[1]], 'name':line.split()[2]}
            if len(line.split()) > 3:
                m['comment'] = ' '.join(line.split()[3:])
            else:
                m['comment'] = ""
            c['members'].append(m)
        elif line.startswith('property'):
            p = {'name':line.split()[1]}
            c['properties'].append(p)
        elif line.startswith('new'):
            c['new'] = True
        elif line.startswith('init'):
            c['init'] = True
        elif line.startswith('dealloc'):
            c['dealloc'] = True
            
for c in classes:
    writeClass(c)