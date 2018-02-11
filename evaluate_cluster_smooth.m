function[] = evaluate_cluster_smooth(clusMethod);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Evaluate clustering results of each column independently.
% clusMethod: k - kmeans, x - xmeans
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

datafolder = '../Data/';

% load clustering results
load([datafolder, 'cluster_smooth.mat']);

if strcmp(clusMethod, 'k')
    % use kmeans to project to 1D
    n = size(C, 1);
    k = int32(sqrt(n/2));
    Ckmeans = kmeans(C, k);
elseif strcmp(clusMethod, 'x')
    mFile = [datafolder, 'cluster_smooth.mat'];
    cFile = [datafolder, 'cluster_smooth.clus'];
    %disp(['./run_xmeans.sh ', mFile, ' ', cFile])
    system(['sythetic-no-mapping/run_xmeans.sh ', mFile, ' ', cFile]);
end

% print time series term
termStruc = norm(Xstruc - C * W, 'fro') ^ 2
termCont = norm(Xcont - C * W, 'fro') ^ 2

% print smoothness term
D = diag(sum(A));
L = D - A;
termSmooth = trace(C' * L * C)

save('evaluation.mat');

% compute nodes in each cluster
clusTbl = cell2table(tabulate(categorical(Ckmeans)));
clusTbl = sortrows(clusTbl, 2, 'descend');
trueClusTbl = cell2table(tabulate(categorical(trueC)));
trueClusTbl = sortrows(trueClusTbl, 2, 'descend');
nodeCnt = clusTbl(:, 2);
nodeCnt = nodeCnt.Var2'

exit;
end
