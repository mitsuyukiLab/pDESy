#!/usr/bin/python
# -*- coding: utf-8 -*-

from pDESy.model.worker import Worker
from pDESy.model.team import Team
from pDESy.model.task import Task
from pDESy.model.base_task import BaseTaskState
from pDESy.model.base_resource import BaseResourceState

import pytest


def test_init():
    team = Team("team")
    w = Worker("w1", team.ID)
    assert w.name == "w1"
    assert w.team_id == team.ID
    assert w.cost_per_time == 0.0
    assert w.workamount_skill_mean_map == {}
    assert w.workamount_skill_sd_map == {}
    assert w.quality_skill_mean_map == {}
    assert w.state == BaseResourceState.FREE
    assert w.cost_list == []
    assert w.start_time_list == []
    assert w.finish_time_list == []
    assert w.assigned_task_list == []


def test_str():
    print(Worker("w1"))


def test_initialize():
    team = Team("team")
    w = Worker("w1", team.ID)
    w.state = BaseResourceState.WORKING
    w.cost_list = [9.0, 7.2]
    w.start_time_list = [0]
    w.finish_time_list = [1]
    w.assigned_task_list = [Task("task")]
    w.initialize()
    assert w.state == BaseResourceState.FREE
    assert w.cost_list == []
    assert w.start_time_list == []
    assert w.finish_time_list == []
    assert w.assigned_task_list == []


# def test_set_workamount_skill_mean_map():
#     w = Worker("w1", "----")
#     w.set_workamount_skill_mean_map(
#         {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True
#     )
#     assert w.workamount_skill_mean_map == {"task1": 1.0, "task2": 0.0}
#     assert w.workamount_skill_sd_map == {"task1": 0.0, "task2": 0.0}
#     assert w.quality_skill_mean_map == {"task1": 0.0, "task2": 0.0}

#     w.set_workamount_skill_mean_map({"task3": 0.5, "task1": 0.5})
#     w.quality_skill_mean_map["task3"] = 1.0
#     assert w.workamount_skill_mean_map == {"task1": 0.5, "task3": 0.5}
#     assert w.workamount_skill_sd_map == {"task1": 0.0, "task2": 0.0}
#     assert w.quality_skill_mean_map == {"task1": 0.0, "task2": 0.0, "task3": 1.0}

#     w.set_workamount_skill_mean_map(
#         {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True,
#     )
#     assert w.workamount_skill_mean_map == {"task1": 1.0, "task2": 0.0}
#     assert w.workamount_skill_sd_map == {"task1": 0.0, "task2": 0.0}
#     assert w.quality_skill_mean_map == {"task1": 0.0, "task2": 0.0}


# def test_set_quality_skill_mean_map():
#     w = Worker("w1", "----")
#     w.set_quality_skill_mean_map(
#         {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True
#     )
#     assert w.quality_skill_mean_map == {"task1": 1.0, "task2": 0.0}
#     assert w.quality_skill_sd_map == {"task1": 0.0, "task2": 0.0}
#     assert w.quality_skill_mean_map == {"task1": 0.0, "task2": 0.0}

#     w.set_quality_skill_mean_map({"task3": 0.5, "task1": 0.5})
#     w.quality_skill_mean_map["task3"] = 1.0
#     assert w.quality_skill_mean_map == {"task1": 0.5, "task3": 0.5}
#     assert w.quality_skill_sd_map == {"task1": 0.0, "task2": 0.0}
#     assert w.quality_skill_mean_map == {"task1": 0.0, "task2": 0.0, "task3": 1.0}

#     w.set_quality_skill_mean_map(
#         {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True,
#     )
#     assert w.quality_skill_mean_map == {"task1": 1.0, "task2": 0.0}
#     assert w.quality_skill_sd_map == {"task1": 0.0, "task2": 0.0}
#     assert w.quality_skill_mean_map == {"task1": 0.0, "task2": 0.0}


def test_has_workamount_skill():
    w = Worker("w1", "----")
    # w.set_workamount_skill_mean_map(
    #     {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True
    # )
    w.workamount_skill_mean_map = {"task1": 1.0, "task2": 0.0}
    assert w.has_workamount_skill("task1")
    assert not w.has_workamount_skill("task2")
    assert not w.has_workamount_skill("task3")


def test_has_quality_skill():
    w = Worker("w1", "----")
    # w.set_quality_skill_mean_map(
    #     {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True
    # )
    w.quality_skill_mean_map = {"task1": 1.0, "task2": 0.0}
    assert w.has_quality_skill("task1")
    assert not w.has_quality_skill("task2")
    assert not w.has_quality_skill("task3")


def test_get_work_amount_skill_point():
    w = Worker("w1", "----")
    # w.set_workamount_skill_mean_map(
    #     {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True
    # )
    w.workamount_skill_mean_map = {"task1": 1.0, "task2": 0.0}
    assert w.get_work_amount_skill_point("task3") == 0.0
    assert w.get_work_amount_skill_point("task2") == 0.0
    with pytest.raises(ZeroDivisionError):
        assert w.get_work_amount_skill_point("task1") == 1.0

    task1 = Task("task1")
    task1.state = BaseTaskState.NONE
    w.assigned_task_list = [task1]
    with pytest.raises(ZeroDivisionError):
        assert w.get_work_amount_skill_point("task1") == 1.0
    task1.state = BaseTaskState.READY
    with pytest.raises(ZeroDivisionError):
        assert w.get_work_amount_skill_point("task1") == 1.0
    task1.state = BaseTaskState.WORKING_ADDITIONALLY
    assert w.get_work_amount_skill_point("task1") == 1.0
    task1.state = BaseTaskState.FINISHED
    with pytest.raises(ZeroDivisionError):
        assert w.get_work_amount_skill_point("task1") == 1.0
    task1.state = BaseTaskState.WORKING
    assert w.get_work_amount_skill_point("task1") == 1.0

    w.workamount_skill_sd_map["task1"] = 0.1
    assert w.get_work_amount_skill_point("task1", seed=1234) == 1.0471435163732492

    task2 = Task("task2")
    task2.state = BaseTaskState.NONE
    w.assigned_task_list.append(task2)
    w.workamount_skill_sd_map["task1"] = 0.0
    assert w.get_work_amount_skill_point("task1") == 1.0
    task2.state = BaseTaskState.WORKING
    assert w.get_work_amount_skill_point("task1") == 0.5


def test_get_quality_skill_point():
    w = Worker("w1", "----")
    # w.set_quality_skill_mean_map(
    #     {"task1": 1.0, "task2": 0.0}, update_other_skill_info=True
    # )
    w.quality_skill_mean_map = {"task1": 1.0, "task2": 0.0}
    assert w.get_quality_skill_point("task3") == 0.0
    assert w.get_quality_skill_point("task2") == 0.0
    assert w.get_quality_skill_point("task1") == 1.0

    task1 = Task("task1")
    task1.state = BaseTaskState.NONE
    w.assigned_task_list = [task1]
    assert w.get_quality_skill_point("task1") == 1.0
    task1.state = BaseTaskState.READY
    assert w.get_quality_skill_point("task1") == 1.0
    task1.state = BaseTaskState.WORKING_ADDITIONALLY
    assert w.get_quality_skill_point("task1") == 1.0
    task1.state = BaseTaskState.FINISHED
    assert w.get_quality_skill_point("task1") == 1.0
    task1.state = BaseTaskState.WORKING
    assert w.get_quality_skill_point("task1") == 1.0

    w.quality_skill_sd_map["task1"] = 0.1
    assert w.get_quality_skill_point("task1", seed=1234) == 1.0471435163732492

    task2 = Task("task2")
    task2.state = BaseTaskState.NONE
    w.assigned_task_list.append(task2)
    w.quality_skill_sd_map["task1"] = 0.0
    assert w.get_quality_skill_point("task1") == 1.0
    task2.state = BaseTaskState.WORKING
    assert w.get_quality_skill_point("task1") == 1.0