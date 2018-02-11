function [C] = gradientDescent(a1, a2, lambda, A, X1, X2, C, W, numIters)
% Gradient Descent is used to learn the parameters theta in order to fit a
% straight line to the points.

% Initialize values
iter = 0;
deltaC = 100;

% step size must be very small
stepSize = 1e-10;

while iter <= numIters & deltaC >= 1e-3
    iter = iter + 1;
    oldC = C
    %disp('first term')
    %(a1 * (C * W - X1) + a2 * (C * W - X2)) * W'
    %disp('second term')
    %(A - C * C') * C
    gradient = 2 * (a1 * (C * W - X1) + a2 * (C * W - X2)) * W' - 4 * lambda * (A - C * C') * C;
    % TODO: update stepSize with Hessian matrix
    %stepSize = 
    C = C - stepSize * gradient;
    deltaC = norm(C - oldC);
end

end
