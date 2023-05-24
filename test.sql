SELECT
                u.id,
                u.first_name || ' ' || u.last_name AS 'full_name',
                g.id as 'game_id',
                g.title,
                g.maker,
                g.skill_level,
                g.number_of_players,
                g.game_type_id
            FROM auth_user u
            JOIN levelupapi_game g ON u.id = g.creator_id


SELECT
                u.id,
                u.first_name || ' ' || u.last_name AS 'full_name',
                g.*
            FROM auth_user u
            JOIN levelupapi_gamer gr ON gr.user_id = u.id
            JOIN levelupapi_game g ON g.creator_id = gr.id

SELECT
                gr.id AS gamer_id,
                u.first_name || ' ' || u.last_name AS full_name,
                g.*
            FROM levelupapi_game g
            JOIN levelupapi_gamer gr
                ON g.creator_id = gr.id
            JOIN auth_user u
                ON gr.user_id = u.id


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