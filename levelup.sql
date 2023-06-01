CREATE VIEW GAMES_BY_USER AS
SELECT
    g.id,
    g.title,
    g.maker,
    g.game_type_id,
    g.number_of_players,
    g.skill_level,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN
    levelupapi_gamer gr ON g.creator_id = gr.id
JOIN
    auth_user u ON gr.user_id = u.id
;


CREATE VIEW EVENTS_BY_USER AS
SELECT
                gr.id AS gamer_id,
                u.first_name || ' ' || u.last_name AS full_name,
                g.title AS game,
                e.*
            FROM levelupapi_event e
            JOIN levelupapi_event_attendees ea 
                ON ea.event_id = e.id
            JOIN levelupapi_gamer gr
                ON ea.gamer_id = gr.id
            JOIN auth_user u
                ON gr.user_id = u.id
            JOIN levelupapi_game g 
                ON e.game_id = g.id
            ORDER BY gamer_id;