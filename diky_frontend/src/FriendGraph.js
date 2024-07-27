import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';
import { getGraphData } from './apiService';
import { useNavigate } from 'react-router-dom';
const FriendGraph = ({ userId }) => {
    const container = useRef(null);
    const navigate = useNavigate();
    useEffect(() => {
        const fetchGraphData = async () => {
            try {
                const graphData = await getGraphData();
                const edges = graphData.edges;
                const edgeNodeIds = new Set(edges.flatMap(edge => [edge.data.source, edge.data.target]));
                const nodes = graphData.nodes.filter(node => edgeNodeIds.has(node.data.id));

                cytoscape({
    
                    container: container.current,
                    elements: { nodes, edges },
                    style: [
                        {
                            selector: 'node[label]',
                            style: {
                                'background-color': '#666',
                                label: 'data(label)',
                            },
                        },
                        {
                            selector: 'edge',
                            style: {
                                width: 3,
                                'line-color': '#ccc',
                                'target-arrow-color': '#ccc',
                                'target-arrow-shape': 'triangle',
                            },
                        },
                    ],
                    layout: {
                        name: 'grid',
                        rows: 1,
                    },
                });
            } catch (error) {
                console.error('Failed to fetch graph data', error);
            }
        };

        fetchGraphData();
    }, [userId]);
    const handleHomepageClick = () => {
        navigate('/');
    };

    return (
    <div>
        <div ref={container} style={{ height: '1000px' }} />
        <button onClick={handleHomepageClick}>Homepage</button>
    </div>
    );
};

export default FriendGraph;