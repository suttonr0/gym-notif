from gym.envs.registration import register

register(
    id='notif-v0',
    entry_point='gym_notif.envs:NotifEnv',
)