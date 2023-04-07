from typing import Dict
from typing import List

from .base import Logger
# from .base import MarketStepEndLog
from .base import OrderLog


class AgentOrderLogger(Logger):
    """Logger of the agent order class."""

    def process_order_log(self, log: OrderLog) -> None:
        """print the order log.

        Args:
            log (:class:`pams.logs.OrderLog`): order log.

        Returns:
            None
        """
        print(
            f"{log.order_id} {log.agent_id} {log.market_id} {log.time} {log.is_buy} {log.kind} {log.volume} {log.price} {log.ttl}"
        )


class AgentOrderSaver(Logger):
    """Saver of the agent order class."""

    agent_order_logs: List[Dict] = []

    def process_order_log(self, log: OrderLog) -> None:
        """stack the order log.

        Args:
            log (:class:`pams.logs.OrderLog`): order log.

        Returns:
            None
        """
        self.agent_order_logs.append(
            {
                "order_id": log.order_id,
                "agent_id": log.agent_id,
                "market_id": log.market_id,
                "order_time": log.time,
                "is_buy": log.is_buy,
                "kind": log.kind,
                "volume": log.volume,
                "price": log.price,
                "time_exp": log.ttl,
            }
        )
