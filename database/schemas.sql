CREATE TABLE IF NOT EXISTS appointments(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	full_name TEXT NOT NULL,
	phone_number TEXT,
	tg_id TEXT,
	start_time TIME NOT NULL,
	reason TEXT
);