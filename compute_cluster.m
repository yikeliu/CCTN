%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read in matrices and run time-series clustering.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%addpath('jsonlab-1.2/jsonlab/');
addpath('json/');

% if load json file
%Xstruc = loadjson('../Data/structural_matrix.json');

% if load txt file
%Xstruc = dlmread('../Data/structural_matrix.txt.filtered.data');
Xstruc = dlmread('../Data/structural_matrix.json.txt.filtered.data');
%phoneStruc = dataread('file', '../Data/structural_matrix.txt.phones', '%s', 'delimiter', '\n');
phoneStruc = dataread('file', '../Data/structural_matrix.json.txt.filtered.phones', '%s', 'delimiter', '\n');
n = length(Xstruc);
%Xcont = dlmread('../Data/lsh_matrix.txt.filtered.data');
Xcont = dlmread('../Data/lsh_matrix.json.txt.filtered.data');
%Xcont = zeros(size(Xstruc));
phoneCont = dataread('file', '../Data/lsh_matrix.json.txt.filtered.phones', '%s', 'delimiter', '\n');
%phoneCont = Xcont(:, 1);

% reorder X matrices
%fname = '../Data/filtered_index.json';
fname = '../Data/filtered_index.json';
fid = fopen(fname);
raw = fread(fid,inf);
str = char(raw');
fclose(fid);
dict = JSON.parse(str);
%dict = textscan(str, '%s%d', 'delimiter', '\t');
%celldisp(dict);
%for i = 1:length(dict{1})
%    dict{1}(i) = strcat('p', dict{1}(i));
%end
%dict = cell2struct(num2cell(dict{2}), dict{1}, 1);
idxStruc = zeros(n, 1);
idxCont = zeros(n, 1);
for i = 1:n
    phoneNumStruc = char(phoneStruc(i));
    phoneNumCont = char(phoneStruc(i));
    if strcmp(phoneNumStruc(1), 'x')
        phoneNumStruc = matlab.lang.makeValidName(strrep(phoneNumStruc, '-', '_'));
        idxStruc(i) = eval(['dict.',phoneNumStruc]);
    else
        phoneNumStruc = strcat('s', phoneNumStruc);
        phoneNumStruc = matlab.lang.makeValidName(strrep(phoneNumStruc, '-', '_'));
        idxStruc(i) = eval(['dict.', phoneNumStruc]);
    end

    if strcmp(phoneNumCont(1), 'x')
        phoneNumCont = matlab.lang.makeValidName(strrep(phoneNumCont, '-', '_'));
        idxCont(i) = eval(['dict.',phoneNumCont]);
    else
        phoneNumCont = strcat('s', phoneNumCont);
        phoneNumCont = matlab.lang.makeValidName(strrep(phoneNumCont, '-', '_'));
        idxCont(i) = eval(['dict.', phoneNumCont]);
    end
end

Xstruc = Xstruc(idxStruc, :);
Xcont = Xcont(idxCont, :);

% adjacency matrix
A = spconvert(dlmread('../Data/all.phone-page-phone.edges.filtered'));
A(max(size(A)), max(size(A))) = 0;
A = A + A';

[W, C] = Timecluster(Xstruc, Xcont, 10, A, true, true);

save('cluster.mat');

disp(W);
disp(C);

% plot W
time = 1:length(W);
figure
scatter(time, W);
savefig('../Data/W_time.pdf');

% plot C
%tabC = tablulate(C);
%tabC = table2array(tabC);
figure
histogram(C);
savefig('../Data/C_distribution.pdf');



exit;
