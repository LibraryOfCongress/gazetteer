CREATE TABLE woe (
      woeid varchar NOT NULL,
      iso varchar NOT NULL,
      name text NOT NULL,
      language varchar NOT NULL,
      type varchar NOT NULL,
      parent varchar NOT NULL,
      PRIMARY KEY (woeid)
);
CREATE TABLE woe_aliases (
      woeid varchar NOT NULL,
      name text NOT NULL,
      nametype varchar NOT NULL,
      language varchar DEFAULT NULL
);
