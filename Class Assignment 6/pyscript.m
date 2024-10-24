mylist = py.list({'apple', 'banana', 'orange'});
len_of_list = py.len(mylist);
disp(len_of_list);

py_math = py.importlib.import_module('math');
result = py_math.sqrt(25);
disp(result);

py_script = py.importlib.import_module('greet');
greeting = py_script.greet('Abdullah Jarawan');
disp(greeting);