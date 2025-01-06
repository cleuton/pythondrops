CREATE TABLE IF NOT EXISTS pessoa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dependente (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nascimento DATE NOT NULL,
    parentesco VARCHAR(50) NOT NULL,
    id_pessoa INTEGER NOT NULL,
    CONSTRAINT fk_pessoa
        FOREIGN KEY(id_pessoa) 
            REFERENCES pessoa(id)
            ON DELETE CASCADE
);

insert into pessoa (nome) values ('João');
insert into pessoa (nome) values ('Maria');
insert into dependente (nome, nascimento, parentesco, id_pessoa) values ('Filho 1 de João', '2010-01-01', 'Filho', 1);
insert into dependente (nome, nascimento, parentesco, id_pessoa) values ('Filho 2 de João', '2012-01-01', 'Filho', 1);
insert into dependente (nome, nascimento, parentesco, id_pessoa) values ('Filho 1 de Maria', '2014-01-01', 'Filho', 2);
insert into dependente (nome, nascimento, parentesco, id_pessoa) values ('Filho 2 de Maria', '2016-01-01', 'Filho', 2);
