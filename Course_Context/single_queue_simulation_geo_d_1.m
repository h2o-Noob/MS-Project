function[average_occupancy, average_utilization] = single_queue_simulation_geo_d_1(injection_rate, service_time, simulation_length)

% single queue simulation for geo/D/1

%% Initialization of state variables
occupancy_counter = 0;
num_arrivals = 0;
utilization_counter = 0;
is_server_busy = 0;
current_occupancy = 0;
remaining_service_time = 0;



%% Simulation

for cycle = 1:simulation_length


    %% arrival routine
    if (rand <= injection_rate)
        current_occupancy = current_occupancy + 1;
        num_arrivals = num_arrivals + 1;
    else
        
    end

    %% service routine
    if (is_server_busy == 1)
        remaining_service_time = remaining_service_time - 1;
        if (remaining_service_time == 0)
            is_server_busy = 0;
        end
    end

    % putting a packet in the server
    if (is_server_busy == 0 && current_occupancy > 0)
        is_server_busy = 1;
        current_occupancy = current_occupancy - 1;
        remaining_service_time = service_time;
    end

    % updating the counters
    occupancy_counter = occupancy_counter + current_occupancy;
    if (is_server_busy == 1)
        utilization_counter = utilization_counter + 1;
    end

    assert(occupancy_counter >= 0);
    assert(current_occupancy >= 0);

end

%% result collection
average_occupancy = occupancy_counter/simulation_length;
average_utilization = utilization_counter/simulation_length;

end