import React, { useEffect, useState } from 'react';
import api from '../api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
    const [indicators, setIndicators] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await api.get('/indicators/');
                setIndicators(response.data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const logout = () => {
        localStorage.removeItem('token');
        window.location.href = '/';
    };

    if (loading) return <p>Chargement...</p>;

    return (
        <div style={{ padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h1>Tableau de bord EcoTrack</h1>
                <button onClick={logout} style={{ padding: '10px', backgroundColor: '#f44336', color: 'white', border: 'none' }}>Déconnexion</button>
            </div>

            <div style={{ height: '300px', margin: '20px 0' }}>
                <h3>Aperçu des données</h3>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={indicators}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="timestamp" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 8 }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            <h3>Données Détaillées</h3>
            <table border="1" style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Type</th>
                        <th>Valeur</th>
                        <th>Unité</th>
                        <th>Source</th>
                        <th>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {indicators.map((ind) => (
                        <tr key={ind.id}>
                            <td>{ind.id}</td>
                            <td>{ind.type}</td>
                            <td>{ind.value}</td>
                            <td>{ind.unit}</td>
                            <td>{ind.source}</td>
                            <td>{new Date(ind.timestamp).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Dashboard;