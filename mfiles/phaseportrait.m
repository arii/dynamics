function phaseportrait(F, Xmin, Xmax, randomSolutions, spacing, x0List, T)
% Author: Ariel Anders
% 
% Xmin and Xmax are the bounds for the input
% Xmin and Xmax can be a 2x1 or 1x1
% when a 1x1 is used the input bounds for x1 and x2 are the same

%randomSolutions is an integer
% represents the number of random solutions plotted on the phase
% portrait in blue.

%spacing is an integer
% represents the number of arrows plotted in the vector field.
% can be a 2x1 or 1x1 for different dimensions in x1 and x2

%x0List is a nx2 matrix
%each row is a point to plot the solution from

%T is the time period for ODE to plot solutions

close all; hold on 

if nargin ==0
    
    F = @(t,Y) [Y(2); -sin(Y(1))];    
    randomSolutions = 5;
    
    Xmin =  [-2, -2]; % can be 2x1 or 1x1
    Xmax = [8, 2];% can be 2x1 or 1x1
    spacing = [20, 20];% can be 2x1 or 1x1
    x0List = [[0, 0];  [1,1]]; %list of points
    T = [0, 10];
    
    %alternative 1x1 inputs
    %Xmin =  -2; % can be 2x1 or 1x1
    %Xmax = 8;
    %spacing = 20;
    %x0List = [0,0]; % or indivudual point
end

Xmin = doubleInput(Xmin);
Xmax = doubleInput(Xmax);
spacing = doubleInput(spacing);


x1 = linspace(Xmin(1),Xmax(1),spacing(1));
x2 = linspace(Xmin(2),Xmax(2),spacing(2));

[x,y] = meshgrid(x1,x2);

u = zeros(size(x));
v = zeros(size(x));

t=0; 
for i = 1:numel(x)
    Xdot = F(t,[x(i); y(i)]);
    u(i) = Xdot(1);
    v(i) = Xdot(2);
end

samples = rand(randomSolutions, 2);
for i = 1:randomSolutions
 x_1 = Xmin(1) + (Xmax(1) - Xmin(1))*samples(i,1);
 x_2 = Xmin(2) + (Xmax(2) - Xmin(2))*samples(i,2);
 X0 = [x_1, x_2]
 [t, x_t] = ode45(F, T, X0);
 plot (x_t(:,1), x_t(:,2), 'b');
end
for i = 1: (numel(x0List)/2)
    [t, x_t] = ode45(F, T, x0List(i, :));
    plot (x_t(:,1), x_t(:,2), 'g');
end

 
quiver(x,y,u,v,'r'); figure(gcf)
xlabel('y_1')
ylabel('y_2')
axis  tight ;
axis([Xmin(1) Xmax(1) Xmin(2) Xmax(2)])

xlabel('x1 axis')
ylabel('x2 axis')
title('Phase portrait')

    function val = doubleInput(val_in)
        if length(val_in) == 1
            val = [val_in, val_in]
        elseif length(val_in) == 2
            val = val_in
        else
            error("inputs are incorrect")
        end
    end


end
