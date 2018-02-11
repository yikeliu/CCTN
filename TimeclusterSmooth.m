function[W, C, CReal, success] = TimeclusterSmooth(X1, X2, iter, a1, a2, lambda, G, roundC, random, stoch, f)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% X1: structural matrix
% X2: content matrix
% a1: weight for struct matrix
% a2: weight for cont matrix
% lambda: weight for first regularization
% f: number of features
% G: adjacency matrix of graph
% n: number of data points
% T: number of time stamps
% iter: maximum number of iterations
% roundC: true if round C in every iteration
% random: if update of rows in each iteration is randomized
% stoch: if only pick one row to update or update all rows
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Options for the Kaczmarz algorithm
kiter = 1000;
kprecision = 0.5*1E-3;
kdisplay = 0;
numIters = 100;
eps = 1e-1;
success = true;
%a1 = 1; % weight for struct matrix
%a2 = 0; % weight for cont matrix
%lambda = 0;

%%
[n,T] = size(X1);
cmax = 1;
if size(X2,1) ~= n && size(X2,2) ~= T
    error('error for dimension Y');
end
%% random initialization
C = ones(n,f);
for i = 1:n
    for j = 1:f
        %C(i, j) = round(rand()*length(C)) + 1;
        C(i, j) = ceil(rand()*n);
    end
end
% each node in its own cluster
%C = 1:n;
%C = repmat(C', 1, f);
% initialize true cluster
%C = [ones(100, 1); 100 * ones(100, 1); 200 * ones(200, 1)];
%C = [ones(100, f); 100 * ones(50, f); 200 * ones(200, f)];
%disp(C);
%W = rand(T,1); %1/T*ones(T, 1); %rand(T,1) % change to uniform weights?
W = rand(f, T); %1/T*ones(T, 1); %rand(T,1) % change to uniform weights?
%D = diag(diag(G));
D = diag(sum(G, 1));
%disp(size(D));
L = D - G;
[row, col] = find(G);
B = zeros(n);
B([row, col]) = 1;
Bsup = ones(n) - B - diag(ones(n, 1));
DBsup = diag(sum(Bsup, 1));
LBsup = DBsup - Bsup;
I = eye(n, n);
%for r = 1:iter
t = 0;
%while norm(W - WOld, 1) <= 1e-3 & (norm(C - COld, 1) <= 10 | t <= iter)
tic
%while t <= iter
while t <= iter & (norm(W - WOld, 1) >= eps | norm(C - COld, 1) >= eps)
    t = t + 1
    WOld = W;
    COld = C;
    % fix C, update W
    %A = a1 * X1' * X1 + a2 * X2' * X2;
    A = (a1 + a2) * C' * C;
    %size(C)
    %size(X1)
    %size(X2)
    b = a1 * C' * X1 + a2 * C' * X2;
    if random == true
        if stoch == true
            %W = RKinverseAll(A, a1 * X1' * C + a2 * X2' * C, W, [kiter, 1, kprecision, kdisplay, 1]);
            W = RKinverseAll(A, b, W, [kiter, 1, kprecision, kdisplay, 1]);
        else
            %W = RKinverseAll(A, a1 * X1' * C + a2 * X2' * C, W, [kiter, 1, kprecision, kdisplay, 0]);
            try
                W = RKinverseAll(A, b, W, [kiter, 1, kprecision, kdisplay, 0]);
            catch
                warning('This case does not run!');
                success = false;
                break;
            end
        end
    else
        if stoch == true
            %W = RKinverseAll(A, a1 * X1' * C + a2 * X2' * C, W, [kiter, 0, kprecision, kdisplay, 1]);
            W = RKinverseAll(A, b, W, [kiter, 0, kprecision, kdisplay, 1]);
        else
            %W = RKinverseAll(A, a1 * X1' * C + a2 * X2' * C, W, [kiter, 0, kprecision, kdisplay, 0]);
            W = RKinverseAll(A, b, W, [kiter, 0, kprecision, kdisplay, 0]);
        end
    end
    % project W to positive range
    W = max(0, W);

    % fix W, update C
    %A = [lambda * L, eye(n)];
    %b = norm([eye(f), (a1 + a2) * W * W']) ^ (-2) * (a1 * X1 + a2 * X2) * W' * [eye(f), (a1 + a2) * W * W'];
    %C2 = [C, zeros(n, f); zeros(n, f), C];
    %if random == true
    %    %C = RKinverseAll(2 * lambda * L - 2 * mu / (cmax ^ 2) * LBsup + (a1 + a2) * I, a1 * X1 * W + a2 * X2 * W, C, [kiter, 1, kprecision, kdisplay]);
    %    C2 = RKinverseAll(A, b, C2, [kiter, 1, kprecision, kdisplay, 0]);
    %else
    %    C2 = RKinverseAll(A, x, C2, [kiter, 0, kprecision, kdisplay, 0]);
    %end
    %% check the two components of C2
    %Cleft = C2(1:n, 1:f)
    %Cright = C2((n + 1):end, (f + 1):end)
    %C = mean(cat(3, C2(1:n, 1:f), C2((n + 1):end, (f + 1):end)), 3)
    %C = gradientDescent(a1, a2, lambda, G, X1, X2, C, W, numIters);
    A = lambda * L;
    B = (a1 + a2) * W * W';
    C = (a1 * X1 + a2 * X2) * W';
    try
        C = sylvester(full(A), B, C);
    catch
        warning('This case does not run!');
        success = false;
        break;
    end
    %C = lyap(full(A), B, -C);
    % project C to positive range
    C = max(0, C);
    Cdiff = norm(C - COld, 1);
    Wdiff = norm(W - WOld, 1);
    if roundC == true
        C = ceil(C); % change to ceiling?
        C = max(1, C);% remove negative entries
        C = min(n, C);% remove entries greater than n?
        %disp(C);
        %convert C to integer
        %Update U
    end
end
%if roundC == false
%    CReal = C;
%    C = ceil(C); % change to ceiling?
%    C = max(1, C);% remove negative entries
%    C = min(n, C);% remove entries greater than n?
%else
%    CReal = zeros(size(C));
%end
CReal = C;
time = toc
%disp(C);
end

