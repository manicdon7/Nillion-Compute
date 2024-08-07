import asyncio
import py_nillion_client as nillion
import os
import itertools
import sys, random
import re
from py_nillion_client import NodeKey, UserKey
from dotenv import load_dotenv
from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey
from nillion_python_helpers import get_quote_and_pay, create_nillion_client, create_payments_config

class NadaPublish:
    def __init__(self, EnvPath: str, Seed: str, PrgBinMirPath: str, ProgramName: str) -> None:
        """
        Initialize NadaPublish with environment path.
        """
        # Load Variables
        load_dotenv(EnvPath)
        self.env = EnvPath
        self.Seed = Seed
        self.PrgBinMirPath = PrgBinMirPath
        self.cluster_id = os.getenv("NILLION_CLUSTER_ID")
        self.grpc_endpoint = os.getenv("NILLION_NILCHAIN_GRPC")
        self.chain_id = os.getenv("NILLION_NILCHAIN_CHAIN_ID")

        # Initialize Nillion
        userkey = UserKey.from_seed(Seed)
        nodekey = NodeKey.from_seed(Seed)
        self.client = create_nillion_client(userkey, nodekey)
        self.party_id = self.client.party_id
        self.user_id = self.client.user_id
        self.ProgramName = ProgramName
        payments_config = create_payments_config(self.chain_id, self.grpc_endpoint)
        self.payments_client = LedgerClient(payments_config)
        self.payments_wallet = LocalWallet(
            PrivateKey(bytes.fromhex(os.getenv("NILLION_NILCHAIN_PRIVATE_KEY_0"))),
            prefix="nillion",
        )

    async def StoreProgram(self, PartyName: str, VariablenameWithValue: dict, verbose: bool = False):
        output = []
        plain_output = []

        def custom_print(*args, emoji="", color_code="\033[94m", verbose=verbose):
            message = " ".join(map(str, args))
            log_message = f"{emoji} {message}"
            colored_message = f"{color_code}{log_message}\033[0m"
            plain_output.append(log_message)
            if verbose:
                print(colored_message)

        async def spinner():
            for c in itertools.cycle(random.choice([['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'], ['-', '=', '≡'], ['▖', '▘', '▝', '▗'],['▁', '▂', '▃', '▅', '▆', '▇', '█'], ['❤', '💛', '💚', '💙', '💜'],['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈']])):
                if not spinning:
                    break
                sys.stdout.write(f'\rLoading... {c}')
                sys.stdout.flush()
                await asyncio.sleep(0.1)
            sys.stdout.write('\rDone!     \n')

        # Get cost quote, then pay for operation to store program
        custom_print("Initiating program storage...", emoji="🚀", color_code="\033[94m")

        spinning = True
        spinner_task = asyncio.create_task(spinner())

        receipt_store_program = await get_quote_and_pay(
            self.client,
            nillion.Operation.store_program(self.PrgBinMirPath),
            self.payments_wallet,
            self.payments_client,
            self.cluster_id,
        )

        # Store program, passing in the receipt that shows proof of payment
        action_id = await self.client.store_program(
            self.cluster_id, self.ProgramName, self.PrgBinMirPath, receipt_store_program
        )

        spinning = False
        await spinner_task

        program_id = f"{self.user_id}/{self.ProgramName}"
        custom_print("Stored program. action_id:", action_id, emoji="✅", color_code="\033[92m")
        custom_print("Stored program_id:", program_id, emoji="✅", color_code="\033[92m")

        custom_print("STORE PROGRAM", emoji="-----", color_code="\033[93m")

        for i, j in VariablenameWithValue.items():
            VariablenameWithValue[i] = nillion.SecretInteger(j)

        LenofDict = len(VariablenameWithValue)
        FirstHalfVal = abs(int(LenofDict / 2))

        SecondHalf = dict(list(VariablenameWithValue.items())[:FirstHalfVal])
        FirstHalf = dict(list(VariablenameWithValue.items())[FirstHalfVal:])

        custom_print("FirstHalf:", FirstHalf, "SecondHalf:", SecondHalf, emoji="📊", color_code="\033[96m")
        
        stored_secret = nillion.NadaValues(FirstHalf)
        # Create a permissions object to attach to the stored secret
        permissions = nillion.Permissions.default_for_user(self.client.user_id)
        permissions.add_compute_permissions({self.client.user_id: {program_id}})

        # Get cost quote, then pay for operation to store the secret
        custom_print("Getting quote and paying for storing secrets...", emoji="💰", color_code="\033[95m")

        spinning = True
        spinner_task = asyncio.create_task(spinner())

        receipt_store = await get_quote_and_pay(
            self.client,
            nillion.Operation.store_values(stored_secret, ttl_days=5),
            self.payments_wallet,
            self.payments_client,
            self.cluster_id,
        )
        store_id = await self.client.store_values(
            self.cluster_id, stored_secret, permissions, receipt_store
        )

        spinning = False
        await spinner_task

        compute_bindings = nillion.ProgramBindings(program_id)
        compute_bindings.add_input_party(PartyName, self.party_id)
        compute_bindings.add_output_party(PartyName, self.party_id)

        computation_time_secrets = nillion.NadaValues(SecondHalf)
        # Get cost quote, then pay for operation to compute
        custom_print("Preparing to compute...", emoji="🧠", color_code="\033[95m")

        spinning = True
        spinner_task = asyncio.create_task(spinner())

        receipt_compute = await get_quote_and_pay(
            self.client,
            nillion.Operation.compute(program_id, computation_time_secrets),
            self.payments_wallet,
            self.payments_client,
            self.cluster_id,
        )

        # Compute, passing all params including the receipt that shows proof of payment
        uuid = await self.client.compute(
            self.cluster_id,
            compute_bindings,
            [store_id],
            computation_time_secrets,
            receipt_compute,
        )

        spinning = False
        await spinner_task

        custom_print(f"Computing using program {program_id}", emoji="🖥️", color_code="\033[92m")
        custom_print(f"Use secret store_id: {store_id}", emoji="🔐", color_code="\033[92m")

        custom_print(f"The computation was sent to the network. compute_id: {uuid}", emoji="📡", color_code="\033[93m")
        while True:
            compute_event = await self.client.next_compute_event()
            if isinstance(compute_event, nillion.ComputeFinishedEvent):
                custom_print(f"Compute complete for compute_id {compute_event.uuid}", emoji="✅", color_code="\033[92m")
                custom_print(f"The result is {compute_event.result.value}", emoji="🖥️", color_code="\033[92m")
                log_output = "\n".join(plain_output)
                return log_output, compute_event.result.value

# # Example of how to run the StoreProgram function
# async def main():
#     publish = NadaPublish(".env", "sample seed", "./MatchingAlgo.nada.bin", "MatchingAlgo")
#     log, result = await publish.StoreProgram("MatchParty", {"age_int2": 18, "location_int1": 2, "Match_gender_int": 0, "age_int1": 30, "looking_for_gender_int": 0}, verbose=True)
#     print(f"Computation result: {result}")
#     print(f"Log: \n{log}")

# # Run the async main function
# asyncio.run(main())
