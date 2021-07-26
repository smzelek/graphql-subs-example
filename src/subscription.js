import React, { useEffect, useState, useCallback } from "react";
import { gql, useQuery, useSubscription } from "@apollo/client";
import "./subscription.css";

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

function PollingQuery({ jobId }) {
  const polling = useQuery(BUILD_LOG_QUERY, {
    variables: { jobId: jobId },
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

  useEffect(() => {
    let logs = document.querySelectorAll('.log')
    logs.forEach((log) => {
      log.scrollTop = log.scrollHeight
    })
  });

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

function Subscription({ jobId }) {
  const subscription = useSubscription(SAMPLE_SUBSCRIPTION, {
    variables: { jobId: jobId },
  });
  console.log(subscription);


  return (
    <div className="block">
      <h3>Subscription</h3>
      <p>Server: {subscription.data?.build?.serverName}</p>
      <p>Subscribed to redis event bus serverside</p>
      <p>Result:</p>
      <p className="log">{subscription.data?.build?.buildLog}</p>
    </div>
  );
}

function AppendToBuildLog({ jobId }) {
  const sendRequest = useCallback(async () => {
    await fetch(`http://localhost:5000/append/${jobId}`);
  }, []);

  return (
    <div>
      <button onClick={() => sendRequest()}>sendRequest</button>
    </div>
  );
}

export function Queries() {
  return (
    <div>
      {["3"].map(jobId => (
        <div key={jobId} className="queries">
        <PollingQuery jobId={jobId}/>
        <Subscription jobId={jobId}/>
        <AppendToBuildLog jobId={jobId}/>
      </div>
      ))}
    </div>
  );
}
