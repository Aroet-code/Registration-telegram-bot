-- name: add_appointment
INSERT INTO appointments (full_name, phone_number, tg_id, start_time, reason)
VALUES (:full_name, :phone_number, :tg_id, :start_time, :reason);