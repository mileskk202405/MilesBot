class CmdKit:
    """
    A class to handle command routing operations.
    """

    @staticmethod
    def get_cmd(cmd_merge):
        """
        Extract the high 16 bits from the merged command.

        :param cmd_merge: Merged command from which to extract the high 16 bits.
        :return: The value of the high 16 bits.
        """
        return cmd_merge >> 16

    @staticmethod
    def get_sub_cmd(cmd_merge):
        """
        Extract the low 16 bits from the merged command.

        :param cmd_merge: Merged command from which to extract the low 16 bits.
        :return: The value of the low 16 bits.
        """
        return cmd_merge & 0xFFFF

    @staticmethod
    def merge(cmd, sub_cmd):
        """
        Merge two parameters into a single value, with the first parameter in the high 16 bits and the second in the low 16 bits.

        :param cmd: The main command to be placed in the high 16 bits. Must not exceed 32767.
        :param sub_cmd: The sub-command to be placed in the low 16 bits. Must not exceed 65535.
        :return: The merged result.
        """
        return (cmd << 16) + sub_cmd


# Example usage:
# if __name__ == "__main__":
#     cmd_kit = CmdKit()
#     cmd_merge = cmd_kit.merge(1, 1)
#     print(f"Merged Command: {cmd_merge}")
#     print(f"Command: {cmd_kit.get_cmd(cmd_merge)}")
#     print(f"Sub-Command: {cmd_kit.get_sub_cmd(cmd_merge)}")