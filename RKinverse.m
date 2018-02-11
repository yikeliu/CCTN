function[X] = RKinverse(A, B, X)
% Using Kaczmarz algorithm to compute the X from AX = B;
% X = inv(A) * B;
% X = A\B;
%tic
iter = 100;
m = size(A, 1);
n = size(X, 1);
if size(B, 1) ~= n && size(B, 2) ~= 1
    error('the dimension does not match');
end

a = sum(A.^2,2);
%disp(size(a))

for i = 1:iter
    C = (B - A * X) ./ a;
    %for j = 1:m
       %a = A(j, :);
       %Anorm = a * a';
       %disp(Anorm);
       %X = X + (B(j) - A(j, :) * X) * A(j, :)' ./ a(j);
    %end
    X = X + (C' * A)';
end
%t = toc
end

