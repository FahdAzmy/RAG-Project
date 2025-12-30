# Mini-rag

## Requirements

- python 3.10 or later

#### Install Python using MiniConda

1. Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2. Create a new environment using the following command:

```bash
$ conda create -n mini-rag python=3.8
```

3. Activate the environment:

```bash
$ conda activate mini-rag
```

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Running Docker Services

The project uses Docker to manage the database (MongoDB).

1. **Setup Docker Environment Variables**:
   Create a `.env` file inside the `docker` directory with the following variables:
   ```env
   MONGO_INITDB_ROOT_USERNAME=your_username
   MONGO_INITDB_ROOT_PASSWORD=your_password
   ```

2. **Start the Services**:
   Run the following command from the root directory:
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

3. **Verify Status**:
   You can check if the container is running using:
   ```bash
   docker ps
   ```

