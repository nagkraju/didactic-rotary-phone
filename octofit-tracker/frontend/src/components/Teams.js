import React, { useEffect, useState } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const endpoint = `${process.env.REACT_APP_CODESPACE_NAME ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/` : '/api/teams/'}`;

  useEffect(() => {
    console.log('Fetching Teams from:', endpoint);
    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        const results = data.results || data;
        setTeams(results);
        console.log('Fetched Teams:', results);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching teams:', err);
        setLoading(false);
      });
  }, [endpoint]);

  if (loading) return <div className="text-center my-4">Loading Teams...</div>;

  return (
    <div className="card shadow mb-4">
      <div className="card-header bg-primary text-white">
        <h2 className="h4 mb-0">Teams</h2>
      </div>
      <div className="card-body">
        <div className="table-responsive">
          <table className="table table-striped table-bordered align-middle">
            <thead className="table-light">
              <tr>
                {teams.length > 0 && Object.keys(teams[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {teams.map((team, idx) => (
                <tr key={team.id || idx}>
                  {Object.values(team).map((val, i) => (
                    <td key={i}>{typeof val === 'object' ? JSON.stringify(val) : val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {teams.length === 0 && <div className="text-center">No teams found.</div>}
        </div>
      </div>
    </div>
  );
};

export default Teams;
