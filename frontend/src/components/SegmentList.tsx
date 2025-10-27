import { Fragment } from "react";
import type { TranscriptionResponse } from "../lib/api";

type Props = {
  segments: TranscriptionResponse["segments"];
};

export function SegmentList({ segments }: Props): JSX.Element {
  if (!segments.length) {
    return (
      <section className="card">
        <h2>話者別ログ</h2>
        <p>セグメントが存在しません。</p>
      </section>
    );
  }

  return (
    <section className="card">
      <h2>話者別ログ</h2>
      <ul className="segments">
        {segments.map((segment, index) => (
          <Fragment key={`${segment.speaker}-${index}`}>
            <li className="segment">
              <div className="segment-header">
                <span className="segment-speaker">{segment.speaker}</span>
                <span className="segment-time">
                  {formatTime(segment.start)} - {formatTime(segment.end)}
                </span>
              </div>
              <p>{segment.text}</p>
            </li>
          </Fragment>
        ))}
      </ul>
    </section>
  );
}

function formatTime(value: number): string {
  const minutes = Math.floor(value / 60);
  const seconds = Math.floor(value % 60);
  return `${minutes}:${seconds.toString().padStart(2, "0")}`;
}
