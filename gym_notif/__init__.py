from gym.envs.registration import register

register(
    id='notifenv-v0',
    entry_point='gym_notif.envs:NotifEnv',
)