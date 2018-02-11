function [WInc, CInc, success] = TimeclusterInc(A, AInc, X1, X1Inc, X2, X2Inc, a1, a2, lambda, W, C)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Compute W and C using incremental algorithm.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

success = true;
iter = 100;
eps = 1e-3;
% fix dimensions
[n, t] = size(X1);
[nInc, tInc] = size(X1Inc);
f = size(C, 2);
D = diag(sum(A, 1));
L = D - A;
DInc = diag(sum(AInc, 1));
LInc = DInc - AInc;

CInc = C;
if nInc > n
    CInc(n:nInc, :) = 1;
    for i = n:nInc
        for j = 1:f
            CInc(i, j) = ceil(rand() * nInc);
        end
    end
end

%WInc = W;
%if tInc > t
%    W(:, t:tInc) = rand(f, tInc - t);
%end

X1(nInc, tInc) = 0;
X2(nInc, tInc) = 0;
L(nInc, nInc) = 0;
C(nInc, f) = 0;
W(f, tInc) = 0;

it = 0;
WInc = W;
CInc = C;
WOldInc = zeros(f, tInc);
COldInc = zeros(nInc, f);
tic
while it <= iter & (norm(WInc - WOldInc, 1) >= eps | norm(CInc - COldInc, 1) >= eps)
    it = it + 1
    WOldInc = WInc;
    COldInc = CInc;

    % compute WInc
    deltaX1 = X1Inc - X1;
    deltaX2 = X2Inc - X2;
    deltaW = inv((a1 + a2) * CInc' * CInc) * (a1 * CInc' * deltaX1 + a2 * CInc' * deltaX2);

    % compute CInc
    deltaL = LInc - L;
    deltaW = WInc - W;
    a = lambda * L;
    b = (a1 + a2) * W * W';
    c = a1 * (X1 * deltaW' + deltaX1 * W') + a2 * (X2 * deltaW' + deltaX2 * W') + (a1 + a2) * (lambda * deltaL * C - C * deltaW * W' - C * W * deltaW');

    %size(a)
    %size(b)
    %size(c)

    try
        deltaC = sylvester(full(a), b, c);
    catch
        warning('This case does not run!');
        success = false;
    end
end

WInc = W + deltaW;
CInc = C + deltaC;

runtime = toc

end
