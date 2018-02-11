%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read in matrices and run time-series clustering.
% Cluster on structural matrices only. Separate degree and pagerank matrices.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%addpath('jsonlab-1.2/jsonlab/');
addpath('json/');

% if load json file
%Xstruc = loadjson('../Data/structural_matrix.json');

% if load txt file
Xdegree = dlmread('../Data/degree_matrix.txt.filtered.data');
%Xstruc = dlmread('../Data/structural_matrix.json.txt.filtered.data');
phoneDg = dataread('file', '../Data/degree_matrix.txt.filtered.phones', '%s', 'delimiter', '\n');
%phoneStruc = dataread('file', '../Data/structural_matrix.json.txt.filtered.phones', '%s', 'delimiter', '\n');
n = length(Xdegree);
Xpagerank = dlmread('../Data/pagerank_matrix.txt.filtered.data');
%Xcont = dlmread('../Data/lsh_matrix.json.txt.filtered.data');
%Xcont = zeros(size(Xstruc));
%phoneCont = dataread('file', '../Data/lsh_matrix.json.txt.filtered.phones', '%s', 'delimiter', '\n');
phonePr = dataread('file', '../Data/pagerank_matrix.txt.filtered.phones', '%s', 'delimiter', '\n');
%phoneCont = Xcont(:, 1);

% reorder X matrices
fname = '../Data/filtered_index_struc.json';
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
idxDg = zeros(n, 1);
idxPr = zeros(n, 1);
for i = 1:n
    phoneNumDg = char(phoneDg(i));
    phoneNumPr = char(phonePr(i));
    if strcmp(phoneNumDg(1), 'x')
        phoneNumDg = matlab.lang.makeValidName(strrep(phoneNumDg, '-', '_'));
        idxDg(i) = eval(['dict.',phoneNumDg]);
    else
        phoneNumDg = strcat('s', phoneNumDg);
        phoneNumDg = matlab.lang.makeValidName(strrep(phoneNumDg, '-', '_'));
        idxDg(i) = eval(['dict.', phoneNumDg]);
    end

    if strcmp(phoneNumPr(1), 'x')
        phoneNumPr = matlab.lang.makeValidName(strrep(phoneNumPr, '-', '_'));
        idxPr(i) = eval(['dict.',phoneNumPr]);
    else
        phoneNumPr = strcat('s', phoneNumPr);
        phoneNumPr = matlab.lang.makeValidName(strrep(phoneNumPr, '-', '_'));
        idxPr(i) = eval(['dict.', phoneNumPr]);
    end
end

Xdegree = Xdegree(idxDg, :);
Xpagerank = Xcont(idxPr, :);

% adjacency matrix
A = spconvert(dlmread('../Data/all.phone-page-phone.edges.struc_filtered'));
A(max(size(A)), max(size(A))) = 0;
A = A + A';

[W, C] = Timecluster(Xdegree, Xpagerank, 10, A, true, true);

save('cluster_struc.mat');

disp(W);
disp(C);

% plot W
time = 1:length(W);
figure
fig = scatter(time, W);
saveas(gcf, '../Data/W_time_struc.pdf');

% plot C
%tabC = tablulate(C);
%tabC = table2array(tabC);
figure
fig = histogram(C);
saveas(fig, '../Data/C_distribution_struc.pdf');



exit;
