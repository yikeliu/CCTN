function[] = compute_cluster_smooth(aStruc, aCont, lambda, f);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read in matrices and run time-series clustering for labeled data with
% smoothness regularization.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

datafolder = '../Data/';

% load txt file
% pagerank / degree
Xstruc = dlmread([datafolder, 'structural_matrix.txt.filtered.data']);
Xcont = dlmread([datafolder, 'lsh_matrix.txt.filtered.data']);

% adjacency matrix
A = spconvert(dlmread([datafolder, 'all.phone-page-phone.edges.filtered']));
A(max(size(A)), max(size(A))) = 0;
A = A + A';

[W, C, CReal] = TimeclusterSmooth(Xstruc, Xcont, 100, aStruc, aCont, lambda, A, false, true, false, f);

save([datafolder, 'cluster_smooth.mat']);

exit;
end
