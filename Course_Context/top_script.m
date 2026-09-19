clc
clear
close all

%parameter initialization

service_time = 3; %deterministic
injection_rate_array = [0.05:0.05:0.45, 0.49]; %geometric
waiting_time_simulation = zeros(1, length(injection_rate_array));
average_utlization = zeros(1, length(injection_rate_array));
average_occupancy = zeros(1, length(injection_rate_array));
% average_residual_time = zeros(1, length(injection_rate_array));
simulation_length = 1000000;

waiting_time_analytical = zeros(1, length(injection_rate_array));
% residual_time_analytical = zeros(1, length(injection_rate_array));



for injection_rate_idx = 1:length(injection_rate_array)

    injection_rate = injection_rate_array(injection_rate_idx);

    %% simulation
    [average_occupancy(injection_rate_idx), average_utlization(injection_rate_idx)] = single_queue_simulation_geo_d_1(injection_rate, service_time, simulation_length);
    % waiting_time_simulation(injection_rate_idx) = average_occupancy(injection_rate_idx)/injection_rate;

    % %% analytical
    % rho = injection_rate*service_time;
    % waiting_time_analytical(injection_rate_idx) = 0.5*rho*(service_time - 1)/(1 - rho);
    

end

%% compare
figure()
plot(injection_rate_array, average_occupancy, '^k--','MarkerSize',12,'LineWidth',2);
% hold on
% plot(injection_rate_array, waiting_time_analytical, 'bo-','MarkerSize',12,'LineWidth',2);

% legend('Simulation', 'Analytical', 'location', 'northwest', 'FontSize', 12,'fontweight','bold')
xlabel('Injection Rate (packets/cycle)', 'FontSize', 12,'fontweight','bold')
ylabel('Average Occupancy', 'FontSize', 12,'fontweight','bold')
grid on
box on
