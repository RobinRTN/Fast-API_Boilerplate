
--
-- PostgreSQL database dump
--

-- Dumped from database version 15.10 (Debian 15.10-1.pgdg120+1)
-- Dumped by pg_dump version 15.10 (Debian 15.10-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: dev_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO dev_user;

--
-- Name: brands; Type: TABLE; Schema: public; Owner: dev_user
--

CREATE TABLE public.brands (
    id integer NOT NULL,
    name character varying(120) NOT NULL
);


ALTER TABLE public.brands OWNER TO dev_user;

--
-- Name: brands_id_seq; Type: SEQUENCE; Schema: public; Owner: dev_user
--

CREATE SEQUENCE public.brands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.brands_id_seq OWNER TO dev_user;

--
-- Name: brands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev_user
--

ALTER SEQUENCE public.brands_id_seq OWNED BY public.brands.id;


--
-- Name: channel_brand; Type: TABLE; Schema: public; Owner: dev_user
--

CREATE TABLE public.channel_brand (
    channel_id integer NOT NULL,
    brand_id integer NOT NULL
);


ALTER TABLE public.channel_brand OWNER TO dev_user;

--
-- Name: channel_size; Type: TABLE; Schema: public; Owner: dev_user
--

CREATE TABLE public.channel_size (
    channel_id integer NOT NULL,
    size_id integer NOT NULL
);


ALTER TABLE public.channel_size OWNER TO dev_user;

--
-- Name: channels; Type: TABLE; Schema: public; Owner: dev_user
--

CREATE TABLE public.channels (
    id integer NOT NULL,
    name character varying(120) NOT NULL,
    min_price integer,
    max_price integer,
    user_id integer NOT NULL
);


ALTER TABLE public.channels OWNER TO dev_user;

--
-- Name: channels_id_seq; Type: SEQUENCE; Schema: public; Owner: dev_user
--

CREATE SEQUENCE public.channels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.channels_id_seq OWNER TO dev_user;

--
-- Name: channels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev_user
--

ALTER SEQUENCE public.channels_id_seq OWNED BY public.channels.id;


--
-- Name: sizes; Type: TABLE; Schema: public; Owner: dev_user
--

CREATE TABLE public.sizes (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.sizes OWNER TO dev_user;

--
-- Name: sizes_id_seq; Type: SEQUENCE; Schema: public; Owner: dev_user
--

CREATE SEQUENCE public.sizes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sizes_id_seq OWNER TO dev_user;

--
-- Name: sizes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev_user
--

ALTER SEQUENCE public.sizes_id_seq OWNED BY public.sizes.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: dev_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO dev_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: dev_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO dev_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dev_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: brands id; Type: DEFAULT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.brands ALTER COLUMN id SET DEFAULT nextval('public.brands_id_seq'::regclass);


--
-- Name: channels id; Type: DEFAULT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channels ALTER COLUMN id SET DEFAULT nextval('public.channels_id_seq'::regclass);


--
-- Name: sizes id; Type: DEFAULT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.sizes ALTER COLUMN id SET DEFAULT nextval('public.sizes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: dev_user
--

COPY public.alembic_version (version_num) FROM stdin;
23d88932d371
\.


--
-- Data for Name: brands; Type: TABLE DATA; Schema: public; Owner: dev_user
--

COPY public.brands (id, name) FROM stdin;
1	SCOTCH_SODA
2	CARHARTT
3	CARHARTT_WIP
4	YSL
5	FEAR_OF_GOD
6	LEMAIRE
7	ACNE
8	ARKET
9	ARCTERYX
10	MAMMUT
11	PEAK_PERFORMANCE
12	LEVIS
13	LEVIS_STRAUSS
14	NIKE
15	COURREGES
16	PATAGONIA
17	FROM_FUTURE
18	ALLSAINTS
19	ALL_SAINTS
20	DICKIES
21	DR_MARTENS
22	ARTE
23	AMI_PARIS
24	ENCRE
25	GILDAN
26	JERZEES
27	FRUIT_OF_THE_LOOM
28	SCHOTT
29	HANES
30	TOMMY_HILFIGER
31	YEEZY
32	JACK_WOLFSKIN
33	NOBIS
34	MAISON_KITSUNE
35	LOEWE
36	VETEMENTS
37	JUNYA_WATANABE
38	ZEGNA
39	ALEXANDER_MCQUEEN
40	THIERRY_MUGLER
41	VALENTINO
42	BRUNELLO_CUCINELLI
43	LORO_PIANA
44	PRADA
45	FENDI
46	BOTTEGA_VENETA
47	PARAJUMPERS
48	NIKE_ACG
49	PYRENEX
50	SALOMON
51	CRUEL_PANCAKE
52	AUTRY
\.


--
-- Data for Name: channel_brand; Type: TABLE DATA; Schema: public; Owner: dev_user
--

COPY public.channel_brand (channel_id, brand_id) FROM stdin;
\.


--
-- Data for Name: channel_size; Type: TABLE DATA; Schema: public; Owner: dev_user
--

COPY public.channel_size (channel_id, size_id) FROM stdin;
\.


--
-- Data for Name: channels; Type: TABLE DATA; Schema: public; Owner: dev_user
--

COPY public.channels (id, name, min_price, max_price, user_id) FROM stdin;
\.


--
-- Data for Name: sizes; Type: TABLE DATA; Schema: public; Owner: dev_user
--

COPY public.sizes (id, name) FROM stdin;
1	F_XS
2	M_XS
3	F_S
4	M_S
5	F_M
6	M_M
7	F_L
8	M_L
9	F_XL
10	M_XL
11	F_XXL
12	M_XXL
13	W23
14	W24
15	W25
16	W26
17	W27
18	W28
19	W29
20	W30
21	W31
22	W32
23	W33
24	W34
25	W35
26	W36
27	W37
28	W38
29	W39
30	W40
31	33
32	34
33	35
34	36
35	37
36	38
37	39
38	40
39	41
40	42
41	43
42	44
43	45
44	46
45	47
46	48
47	49
48	50
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dev_user
--

COPY public.users (id, email, password_hash, created_at) FROM stdin;
1	robin@gmail.com	scrypt:32768:8:1$ZLK1bkm9BfW5fpgF$1f7b823ff0b87a94c4ebafd7ba48fea1bd6c974660033dd33e5577d0332600054d1fbd504cbd256e34886dfff45e47533ce13bdb57830cca6153cd3b69e00b16	2024-11-14 14:39:32.546023
2	bryan@gmail.com	scrypt:32768:8:1$FDNXP58zXY8x2haA$59fa695c08f520250333eea27c7c56a278d13628cf0ddc6424732cf53436ee7091af83f60e3605e17c75700150c88e47dbfc8a923a9696c51e65a0365ab950f9	2024-11-14 15:03:59.502893
\.


--
-- Name: brands_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev_user
--

SELECT pg_catalog.setval('public.brands_id_seq', 52, true);


--
-- Name: channels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev_user
--

SELECT pg_catalog.setval('public.channels_id_seq', 1, false);


--
-- Name: sizes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev_user
--

SELECT pg_catalog.setval('public.sizes_id_seq', 48, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dev_user
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: brands brands_name_key; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_name_key UNIQUE (name);


--
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (id);


--
-- Name: channel_brand channel_brand_pkey; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channel_brand
    ADD CONSTRAINT channel_brand_pkey PRIMARY KEY (channel_id, brand_id);


--
-- Name: channel_size channel_size_pkey; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channel_size
    ADD CONSTRAINT channel_size_pkey PRIMARY KEY (channel_id, size_id);


--
-- Name: channels channels_pkey; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_pkey PRIMARY KEY (id);


--
-- Name: sizes sizes_name_key; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.sizes
    ADD CONSTRAINT sizes_name_key UNIQUE (name);


--
-- Name: sizes sizes_pkey; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.sizes
    ADD CONSTRAINT sizes_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: channel_brand channel_brand_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channel_brand
    ADD CONSTRAINT channel_brand_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: channel_brand channel_brand_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channel_brand
    ADD CONSTRAINT channel_brand_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channels(id);


--
-- Name: channel_size channel_size_channel_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channel_size
    ADD CONSTRAINT channel_size_channel_id_fkey FOREIGN KEY (channel_id) REFERENCES public.channels(id);


--
-- Name: channel_size channel_size_size_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channel_size
    ADD CONSTRAINT channel_size_size_id_fkey FOREIGN KEY (size_id) REFERENCES public.sizes(id);


--
-- Name: channels channels_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dev_user
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

