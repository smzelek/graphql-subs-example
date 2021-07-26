import React, { useEffect, useState, useCallback } from "react";
import { gql, useQuery, useSubscription } from "@apollo/client";
import "./subscription.css";

const JOB_ID = "4";

const BUILD_LOG_QUERY = gql`
  query BuildLogQuery($jobId: String!) {
    build(jobId: $jobId) {
      serverName
      buildLog
    }
  }
`;

const SAMPLE_SUBSCRIPTION = gql`
  subscription BuildLogSubscription($jobId: String!) {
    build(jobId: $jobId) {
      serverName
      buildLog
    }
  }
`;

function PollingQuery() {
  const polling = useQuery(BUILD_LOG_QUERY, {
    variables: { jobId: JOB_ID },
  });
  const [pollingIn, setPollingIn] = useState(5);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (pollingIn === 0) {
        polling.refetch();
        setPollingIn(5);
      } else {
        setPollingIn(pollingIn - 1);
      }
    }, 1000);

    return () => clearTimeout(timer);
  }, [polling, pollingIn]);

  return (
    <div className="block">
      <h3>Polling Query</h3>
      <p>Server: {polling.data?.build?.serverName}</p>
      <p>Re-polling in {pollingIn}...</p>
      <p>Result:</p>
      <p className="log">{polling.data?.build?.buildLog}</p>
    </div>
  );
}

function Subscription() {
  const subscription = useSubscription(SAMPLE_SUBSCRIPTION, {
    variables: { jobId: JOB_ID },
  });
  console.log(subscription);
  return (
    <div className="block">
      <h3>Subscription</h3>
      <p>Server: {subscription.data?.build?.serverName}</p>
      <p>Polling serverside every second</p>
      <p>Result:</p>
      <p className="log">{subscription.data?.build?.buildLog}</p>
    </div>
  );
}

function AppendToBuildLog() {
  const sendRequest = useCallback(async () => {
    await fetch(`http://localhost:5000/append/${JOB_ID}`);
  }, []);

  return (
    <div>
      <button onClick={() => sendRequest()}>sendRequest</button>
    </div>
  );
}

export function Queries() {
  return (
    <div className="queries">
      <PollingQuery />
      <Subscription />
      <AppendToBuildLog />
    </div>
  );
}
