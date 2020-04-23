#include "route_planner.h"
#include <algorithm>

RoutePlanner::RoutePlanner(RouteModel &model, float start_x, float start_y, float end_x, float end_y): m_Model(model) {
    // Convert inputs to percentage:
    start_x *= 0.01;
    start_y *= 0.01;
    end_x *= 0.01;
    end_y *= 0.01;

    start_node = &m_Model.FindClosestNode(start_x, start_y);
    end_node = &m_Model.FindClosestNode(end_x, end_y);
}   

// CalculateHValue returns the distance from a node to the end_node
float RoutePlanner::CalculateHValue(RouteModel::Node const *node) {
    return node->distance(*end_node);
}

void RoutePlanner::AddNeighbors(RouteModel::Node *current_node) {
    // get neighbors 
    current_node->FindNeighbors();

    // iterate the neighbors and set parent, h_value and g_value
    for (auto &neighbor : current_node->neighbors) {
        neighbor->parent = current_node;
        neighbor->h_value = CalculateHValue(neighbor);
        neighbor->g_value = current_node->g_value + current_node->distance(*neighbor);
        open_list.push_back(neighbor);
        neighbor->visited = true;
    }
}

// Compare is the function callback used in std::sort, sorts in descending order
bool RoutePlanner::Compare(const RouteModel::Node *a, const RouteModel::Node *b) {
    float r1 = a->h_value + a->g_value;
    float r2 = b->h_value + b->g_value;

    return r1 > r2;
}

RouteModel::Node *RoutePlanner::NextNode() {
    // sort the open_list based on f = h + g, in descending order
    std::sort(open_list.begin(), open_list.end(), [](const auto &a, const auto &b) {
        float r1 = a->h_value + a->g_value;
        float r2 = b->h_value + b->g_value;
        return r1 > r2;
    });

    // get the pointer to the lowest f-value node and return it
    RouteModel::Node *in_path_node = open_list.back();
    open_list.pop_back();

    return in_path_node;
}


std::vector<RouteModel::Node> RoutePlanner::ConstructFinalPath(RouteModel::Node *current_node) {
    // Create path_found vector
    distance = 0.0f;
    std::vector<RouteModel::Node> path_found;
    
    while (current_node->parent) {
        path_found.push_back(*current_node);
        distance += current_node->distance(*current_node->parent);
        current_node = current_node->parent;
    }

    path_found.push_back(*current_node);
    distance *= m_Model.MetricScale(); // Multiply the distance by the scale of the map to get meters.

    std::reverse(path_found.begin(), path_found.end());

    return path_found;
}

// start_node - n1 - n2 - n3 - n4 - end_node
void RoutePlanner::AStarSearch() {
 
    // mark the starting node as visited
    start_node->visited = true;
    open_list.push_back(start_node);

    while (!open_list.empty()) {
        // find next best node
        RouteModel::Node *current_node = NextNode();

        // Have we reached our destination?
        if (current_node->distance(*end_node) == 0) {
            m_Model.path =  ConstructFinalPath(current_node);
            return;
        }
        
        AddNeighbors(current_node);
    }
}