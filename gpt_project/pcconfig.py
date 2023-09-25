import pynecone as pc

class GptprojectConfig(pc.Config):
    pass

config = GptprojectConfig(
    app_name="gpt_project",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)