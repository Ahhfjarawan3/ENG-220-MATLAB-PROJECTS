%Configure Python in MATLAB
pyversion('C:/path/to/python.exe');

%Calling Python Functions from MATLAB
mylist = py.list({'apple', 'banana', 'orange'});
len_of_list = py.len(mylist);
disp(len_of_list);

%Using Python Libraries in MATLAB
py_math = py.importlib.import_module('math');
result = py_math.sqrt(25);
disp(result);

%Running Custom Python Scripts
reverse_module = py.importlib.import_module('reverse_string');
my_str = 'Hello MATLAB';
reversed_str = reverse_module.reverse_string(my_str);
disp(reversed_str);
