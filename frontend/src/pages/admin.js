import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

const Admin = () => {
    const [formData, setFormData] = useState({
        type: 'temperature',
        value: '',
        unit: 'C',
        source: 'Manual Input',
        zone_id: '1',
        timestamp: new Date().toISOString()
    });
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/indicators/', formData);
            setMessage('Indicateur ajouté avec succèes !');
            setTimeout(() => navigate('/dashboard'), 1500);
        } catch (error) {
            console.error(error);
            setMessage('Erreur lors de l\'ajout. Pas admin');
        }
    };

    return (
        <div style={{ maxWidth: '500px', margin: '50px auto', padding: '20px', border: '1px solid #ccc' }}>
            <h2>Ajouter un Indicateur (Admin)</h2>
            {message && <p style={{ color: message.includes('Succès') ? 'green' : 'red' }}>{message}</p>}
            
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '10px' }}>
                    <label>Type:</label>
                    <select name="type" value={formData.type} onChange={handleChange} style={{ width: '100%', padding: '8px' }}>
                        <option value="temperature">Température</option>
                        <option value="windspeed">Vitesse du vent</option>
                        <option value="co2">CO2</option>
                        <option value="humidity">Humidité</option>
                    </select>
                </div>

                <div style={{ marginBottom: '10px' }}>
                    <label>Valeur:</label>
                    <input
                        type="number"
                        name="value"
                        value={formData.value}
                        onChange={handleChange}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <div style={{ marginBottom: '10px' }}>
                    <label>Unité:</label>
                    <input
                        type="text"
                        name="unit"
                        value={formData.unit}
                        onChange={handleChange}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <div style={{ marginBottom: '10px' }}>
                    <label>Zone ID (1=Paris, 2=Lyon, 3=Marseille):</label>
                    <input
                        type="number"
                        name="zone_id"
                        value={formData.zone_id}
                        onChange={handleChange}
                        required
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>

                <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#2196F3', color: 'white', border: 'none' }}>
                    Ajouter
                </button>
            </form>
            <button onClick={() => navigate('/dashboard')} style={{ marginTop: '10px', width: '100%', padding: '10px', backgroundColor: '#ccc', border: 'none' }}>
                Retour
            </button>
        </div>
    );
};

export default Admin;