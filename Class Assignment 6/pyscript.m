%Configure Python in MATLAB
pyversion('C:/bin/python19/python.exe');

%Calling Python Functions from MATLAB
mylist = py.list({'apple', 'banana', 'orange'});
len_of_list = py.len(mylist);
disp(len_of_list);

%Using Python Libraries in MATLAB
py_math = py.importlib.import_module('math');
result = py_math.sqrt(25);
disp(result);

%Running Custom Python Scripts
my_str = 'Hello MATLAB';
reversed_str = py.str(my_str(end:-1:1));
disp(reversed_str);
