function X = RKinverseAll(A, B, Xinit, options)
%KACZMARZ Uses Kaczmarz algorithm to estimate output parameters
%   
%   It is to be called by SUGENOTUNE as method
%   for solving to linear problem A * X = B
%   with given initial Xinit.
% 
%   It also accepts additional argument variable 'options':
%       options(1) - maximum number of sweeps (default: 100);
%       options(2) - randomized Kaczmarz algorithm flag (default: 1);
%       options(3) - termination tolerance on step (default: 1E-5);
%       options(4) - info display during sweep (default: 1);
%       options(5) - stochastic algorithm flag (default: 0).
% 
%   See also SUGENOTUNE
% 
%   Example:
%       A = rand(5, 4);
%       B = rand(5, 2);
%       Xinit = zeros(4, 2);
%       X = kaczmarz(A, B, Xinit);

%   Reference: Strohmer, T., and R. Vershynin, A Randomized Kaczmarz
%   Algorithm with Exponential Convergence.

%   Per Konstantin A. Sidelnikov, 2010.

L = size(B, 2);
M = size(A, 1);

% Set options
default_opts = [100, 1, 1E-4, 0, 0];
%if nargin < 4
if nargin < 5
    options = default_opts;
else
    if length(options) < length(default_opts)
        tmp = default_opts;
        tmp(1 : length(options)) = options;
        options = tmp;
    end
    k = find(isnan(options));
    options(k) = default_opts(k);
end
numsweep = options(1);   % sweeps
randomized = options(2); % randomized Kaczmarz flag
steptol = options(3);    % step tolerance
display = options(4);    % display option
stochastic = options(5); % stochastic flag

% Calculate probability mass vector
tmp = A.^2;
pm = sum(tmp, 2) / sum(tmp(:));
% Calculate discrete CDF
F = cumsum(pm);

X = Xinit;
for l = 1 : L
    % Initial parameters
    x = Xinit(:, l);
    
    % Main loop
    b = B(:, l);
    for k = 1 : numsweep
        x_prev = x;
        
        for m = 1 : M
            % Choose row of A at random, with probability 
            % proportional to norm(A(rp, :))^2
            if randomized
                rm = find(F > rand, 1, 'first');
            else
                rm = m;
            end
            a = A(rm, :);
  
            % Update unknowns            
            x = x + (b(rm) - a * x) * a' / (a * a');

            % update the first selected row if stochastic
            if stochastic
                break;
            end
        end
        
        % Check convergence based on
        % current and previous unknown values
        if norm(x - x_prev) / ...
                (1 + max(norm(x), norm(x_prev))) < steptol
            %fprintf('Convergence at sweep %d is designated\n', k);
            break;
        end
        
        if display
            fprintf('%d. Kaczmarz sweep: %d of %d\n', ...
                l, k, numsweep);
        end
    end
    
    X(:, l) = x;
end
